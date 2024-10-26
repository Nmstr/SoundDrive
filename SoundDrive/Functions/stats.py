from PySide6.QtCharts import QBarCategoryAxis, QBarSeries, QChart, QChartView, QValueAxis, QPieSeries, QLineSeries, QDateTimeAxis
from PySide6.QtGui import QPainter, QBrush, QColor, QPen
from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QDateTime
from collections import Counter, defaultdict
from datetime import datetime, timedelta

class BarChart(QWidget):
    def __init__(self, chart_name: str, sets: list, height: int):
        """
        A bar chart
        :param chart_name: The name of the chart
        :param sets: The data to display
        :param height: The height of the chart
        """
        super().__init__()

        self.series = QBarSeries()
        for entry in sets:
            self.series.append(entry)

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle(chart_name)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        self.axis_x = QBarCategoryAxis()
        self.axis_x.append(["Songs"])
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)

        self.axis_y = QValueAxis()
        self.axis_y.setRange(0, height)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.chart.setBackgroundBrush(QBrush(QColor("#2C3035")))

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        layout = QVBoxLayout(self)
        layout.addWidget(self._chart_view)

class PieChart(QWidget):
    def __init__(self, parent: object, chart_name: str, series: QPieSeries, series_mapping: list[int] = None):
        """
        A pie chart
        :param chart_name: The name of the chart
        :param series: The data to display
        """
        self.parent = parent
        self.series = series
        self.series_mapping = series_mapping
        super().__init__()

        self.series.hovered.connect(self.highlight_slice)
        self.series.clicked.connect(self.slice_clicked)
        self.series.setLabelsVisible()

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle(chart_name)
        self.chart.legend().hide()
        self.chart.setBackgroundBrush(QBrush(QColor("#2C3035")))

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._chart_view.setBackgroundBrush(QBrush(QColor("#2C3035")))

        layout = QVBoxLayout(self)
        layout.addWidget(self._chart_view)

    def highlight_slice(self, slice, state):
        if state:
            slice.setExploded()
            slice.setPen(QPen(Qt.darkGreen, 2))
        else:
            slice.setExploded(False)
            slice.setPen(QPen(Qt.white))

    def slice_clicked(self, slice):
        song_id = self.series_mapping[self.series.slices().index(slice)]
        self.parent.display_song_details(song_id)

class LineChart(QWidget):
    def __init__(self, chart_name, series: QLineSeries):
        """
        A line chart
        :param chart_name: The name of the chart
        :param series: The data to display
        """
        self.series = series
        super().__init__()

        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.addSeries(self.series)
        self.chart.setTitle(chart_name)
        self.chart.setBackgroundBrush(QBrush(QColor("#2C3035")))

        # Create and configure the x-axis (date-time axis)
        self.axis_x = QDateTimeAxis()
        self.axis_x.setFormat("yyyy-MM-dd")
        self.axis_x.setTitleText("Date")
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)

        # Create and configure the y-axis (value axis)
        self.axis_y = QValueAxis()
        self.axis_y.setRange(0, max([point.y() for point in self.series.points()]) + 1)
        self.axis_y.setTitleText("Value")
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._chart_view.setBackgroundBrush(QBrush(QColor("#2C3035")))

        layout = QVBoxLayout(self)
        layout.addWidget(self._chart_view)

class StatsPageManager:
    def __init__(self, parent):
        self.parent = parent
        self.history_data = self.parent.db_access.stats.get_history()
        self.parent.ui.timeframe_combo.currentTextChanged.connect(self.load_page)

    def get_selected_timeframe(self) -> int:
        """
        Returns the number of days the selected timeframe has
        :return: The number of days of the timeframe of -1 for no limit
        """
        text = self.parent.ui.timeframe_combo.currentText()
        match text:
            case "Total":
                return -1
            case "Last 12 Months":
                return 365
            case "Last 6 Months":
                return 180
            case "Last 3 Months":
                return 90
            case "Last 30 Days":
                return 30
            case "Last 7 Days":
                return 7
            case "Today":
                return 1

    def trim_history_by_timeframe(self, history: list) -> list:
        """
        Trimes the history to the timeframe specified b y the user inside the timeframe combo box
        :param history: The history to trim
        :return: The trimmed history
        """
        def trim_history_before_day(untrimmed_history: list, day: int) -> list:
            cutoff_date = datetime.now() - timedelta(days=day)
            trimmed_history = [entry for entry in untrimmed_history if datetime.strptime(entry[3], '%Y-%m-%d %H:%M:%S') > cutoff_date]
            return trimmed_history

        timeframe = self.get_selected_timeframe()
        if timeframe == -1:
            return history
        else:
            return trim_history_before_day(history, timeframe)

    def get_most_played_by_time(self, n: int) -> list:
        """
        Gets the n longest played songs by time from the history
        :param n: The amount of songs to retrieve
        :return: The set to display and the highest value
        """
        # Add the times up to get one total time per song
        cleaned_data = {}
        history = self.trim_history_by_timeframe(self.history_data)
        for data in history:
            if cleaned_data.get(data[1]):
                cleaned_data[data[1]] = cleaned_data[data[1]] + data[4]
                continue
            cleaned_data[data[1]] = data[4]
        # Sort and slice to get the correct values
        cleaned_data = sorted(cleaned_data.items(), key=lambda item: item[1], reverse=True)
        cleaned_data = cleaned_data[:n]
        return cleaned_data

    def get_most_played_by_occurrences(self, n: int) -> list:
        """
        Gets the n most played songs from the history data
        :param n: The amount of songs to retrieve
        :return: The set to display and the highest value
        """
        history = self.trim_history_by_timeframe(self.history_data)
        songs = [song[1] for song in history]  # Extract song IDs from history data
        counter = Counter(songs)
        return counter.most_common(n)

    def compress_history_to_daily(self, history: list) -> list:
        """
        Compresses any given history about single songs into daily format
        :param history: The history to compress
        :return: The compressed history
        """
        # Remove elements that are to old
        history = self.trim_history_by_timeframe(history)
        # Remove the first three elements of each entry
        history = [(entry[3], entry[4]) for entry in history]
        # Trim the dates
        history = [(entry[0].split(" ")[0], entry[1]) for entry in history]

        # Add the times up to get one total time per song
        cleaned_history = defaultdict(float)
        for date, time in history:
            cleaned_history[date] += time

        # Specify the first trough the combo box
        timeframe = self.get_selected_timeframe()
        if timeframe == -1:
            first_date = datetime.strptime(history[0][0], '%Y-%m-%d').date()
        else:
            first_date = (datetime.now() - timedelta(days=timeframe)).date()

        # Add the dates that have no entry
        all_dates = [first_date + timedelta(days=i) for i in
                     range((datetime.strptime(max(cleaned_history.keys()), '%Y-%m-%d').date() - first_date).days + 1)]
        final_history = [(date.strftime('%Y-%m-%d'), cleaned_history[date.strftime('%Y-%m-%d')]) if date.strftime(
            '%Y-%m-%d') in cleaned_history else (date.strftime('%Y-%m-%d'), 0.0) for date in all_dates]

        return final_history

    def get_song_times(self, song_id: int) -> tuple[int, int]:
        """
        Gets the time a song was played for in seconds and the times a song was played
        :param song_id: The id of the song
        :return: A tuple of 2 integers which represent the seconds and times played
        """
        song_history = self.parent.db_access.stats.get_history_for_id(song_id)
        song_history = self.trim_history_by_timeframe(song_history)
        time_spend_playing = 0
        for entry in song_history:
            time_spend_playing += entry[4]

        return time_spend_playing, len(song_history)

    def load_page(self):
        self.history_data = self.parent.db_access.stats.get_history()
        # Display most played songs by time
        most_played_by_time_set = self.get_most_played_by_time(10)
        most_played_by_time_series = QPieSeries()
        series_mapping = []
        for element in most_played_by_time_set:
            song_name = self.parent.db_access.songs.query_id(element[0])[1]
            most_played_by_time_series.append(song_name, element[1])
            series_mapping.append(element[0])
        played_songs_by_time_chart = PieChart(self, "Most Played Songs By Time", most_played_by_time_series, series_mapping)

        layout = self.parent.clear_field(self.parent.ui.played_songs_by_time_container, QVBoxLayout, amount_left = 0)
        layout.addWidget(played_songs_by_time_chart)

        # Display most played songs by occurrences
        most_played_by_occurrences_set = self.get_most_played_by_occurrences(10)
        most_played_by_occurrences_series = QPieSeries()
        series_mapping = []  # Used to later change song details on slice clicked
        for element in most_played_by_occurrences_set:
            song_name = self.parent.db_access.songs.query_id(element[0])[1]
            most_played_by_occurrences_series.append(song_name, element[1])
            series_mapping.append(element[0])
        played_songs_by_occurrences_chart = PieChart(self, "Most Played Songs By Occurrences", most_played_by_occurrences_series, series_mapping)

        layout = self.parent.clear_field(self.parent.ui.played_songs_by_occurrences_container, QVBoxLayout, amount_left = 0)
        layout.addWidget(played_songs_by_occurrences_chart)

        # Display song details
        self.display_song_details(most_played_by_time_set[0][0])

    def display_song_details(self, song_id: int) -> None:
        """
        Displays the song details
        :param song_id: The id of the song to be displayed
        :return: None
        """
        song_data = self.parent.db_access.songs.query_id(song_id)
        self.parent.ui.song_detail_name_label.setText("Song Name: " + song_data[1])
        self.parent.ui.song_detail_artist_label.setText("Artist Name: " + song_data[3])
        time_spend_playing, times_played = self.get_song_times(song_id)
        self.parent.ui.song_detail_times_played_label.setText("Time Spend Playing: " + str(timedelta(seconds=time_spend_playing)).split(".")[0])
        self.parent.ui.song_detail_time_spend_label.setText("Times Played: " + str(times_played))

        song_history = self.parent.db_access.stats.get_history_for_id(song_id)
        song_history = self.compress_history_to_daily(song_history)
        song_over_time_series = QLineSeries()
        for element in song_history:
            date_time = QDateTime.fromString(element[0], "yyyy-MM-dd")
            song_over_time_series.append(date_time.toMSecsSinceEpoch(), element[1])
        song_detail_line_chart = LineChart("Time Listened To Song Over Time", song_over_time_series)
        layout = self.parent.clear_field(self.parent.ui.song_detail_line_chart, QVBoxLayout, amount_left = 0)
        layout.addWidget(song_detail_line_chart)
