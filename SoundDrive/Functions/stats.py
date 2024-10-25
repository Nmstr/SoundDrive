from PySide6.QtCharts import QBarCategoryAxis, QBarSeries, QChart, QChartView, QValueAxis, QPieSeries
from PySide6.QtGui import QPainter, QBrush, QColor, QPen
from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from collections import Counter
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

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        layout = QVBoxLayout(self)
        layout.addWidget(self._chart_view)

        self.chart.setBackgroundBrush(QBrush(QColor("#2C3035")))

class PieChart(QWidget):
    def __init__(self, chart_name: str, series: QPieSeries):
        """
        A pie chart
        :param chart_name: The name of the chart
        :param series: The data to display
        """
        self.series = series
        super().__init__()

        self.series.hovered.connect(self.highlight_slice)
        self.series.setLabelsVisible()

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle(chart_name)
        self.chart.legend().hide()

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._chart_view.setBackgroundBrush(QBrush(QColor("#2C3035")))

        layout = QVBoxLayout(self)
        layout.addWidget(self._chart_view)

        self.chart.setBackgroundBrush(QBrush(QColor("#2C3035")))

    def highlight_slice(self, slice, state):
        if state:
            slice.setExploded()
            slice.setPen(QPen(Qt.darkGreen, 2))
        else:
            slice.setExploded(False)
            slice.setPen(QPen(Qt.white))

class StatsPageManager:
    def __init__(self, parent):
        self.parent = parent
        self.history_data = self.parent.db_access.stats.get_history()
        self.parent.ui.timeframe_combo.currentTextChanged.connect(self.load_page)

    def trim_history_by_timeframe(self) -> list:
        def trim_history_before_day(history: list, day: int) -> list:
            cutoff_date = datetime.now() - timedelta(days=day)
            trimmed_history = [entry for entry in history if datetime.strptime(entry[3], '%Y-%m-%d %H:%M:%S') > cutoff_date]
            return trimmed_history

        text = self.parent.ui.timeframe_combo.currentText()
        match text:
            case "Total":
                return self.history_data
            case "Last 12 Months":
                return trim_history_before_day(self.history_data, 365)
            case "Last 6 Months":
                return trim_history_before_day(self.history_data, 180)
            case "Last 3 Months":
                return trim_history_before_day(self.history_data, 90)
            case "Last 30 Days":
                return trim_history_before_day(self.history_data, 30)
            case "Last 7 Days":
                return trim_history_before_day(self.history_data, 7)
            case "Today":
                return trim_history_before_day(self.history_data, 1)

    def get_most_played_by_time(self, n: int) -> list:
        """
        Gets the n longest played songs by time from the history
        :param n: The amount of songs to retrieve
        :return: The set to display and the highest value
        """
        # Add the times up to get one total time per song
        cleaned_data = {}
        history = self.trim_history_by_timeframe()
        for data in history:
            if cleaned_data.get(data[0]):
                cleaned_data[data[0]] = cleaned_data[data[0]] + data[4]
                continue
            cleaned_data[data[0]] = data[4]
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
        history = self.trim_history_by_timeframe()
        songs = [song[1] for song in history]  # Extract song IDs from history data
        counter = Counter(songs)
        return counter.most_common(n)

    def load_page(self):
        # Display most played songs by time
        sets = self.get_most_played_by_time(10)
        most_played_by_time_series = QPieSeries()
        for element in sets:
            song_name = self.parent.db_access.songs.query_id(element[0])[1]
            most_played_by_time_series.append(song_name, element[1])
        played_songs_by_time_chart = PieChart("Most Played Songs By Time", most_played_by_time_series)

        layout = self.parent.clear_field(self.parent.ui.played_songs_by_time_container, QVBoxLayout, amount_left = 0)
        layout.addWidget(played_songs_by_time_chart)

        # Display most played songs by occurrences
        sets = self.get_most_played_by_occurrences(10)
        most_played_by_occurrences_series = QPieSeries()
        for element in sets:
            song_name = self.parent.db_access.songs.query_id(element[0])[1]
            most_played_by_occurrences_series.append(song_name, element[1])
        played_songs_by_occurrences_chart = PieChart("Most Played Songs By Occurrences", most_played_by_occurrences_series)

        layout = self.parent.clear_field(self.parent.ui.played_songs_by_occurrences_container, QVBoxLayout, amount_left = 0)
        layout.addWidget(played_songs_by_occurrences_chart)
