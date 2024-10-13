from PySide6.QtCharts import QBarCategoryAxis, QBarSeries, QBarSet, QChart, QChartView, QValueAxis
from PySide6.QtGui import QPainter, QBrush, QColor
from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QDate
from collections import Counter
import heapq

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

        self.chart.setBackgroundBrush(QBrush(QColor("#23272A")))

def get_n_largest_elements(counter, n):
    return heapq.nlargest(n, counter.items(), key=lambda item: item[1])

def get_n_most_played_songs(history_data: str, n: int, parent: object) -> tuple[list, int]:
    """
    Gets the n most played songs from the history data
    :param history_data: The history data
    :param n: The amount of songs to retrieve
    :param parent: The parent
    :return: The set to display and the highest value
    """
    songs = [song[1] for song in history_data]  # Extract song IDs from history data

    song_counter = Counter(songs)
    largest_elements = get_n_largest_elements(song_counter, n)
    elements_set = []
    for song, count in largest_elements:
        song_data = parent.db_access.songs.query_id(song)
        bar_set = QBarSet(song_data[1])
        bar_set.append(count)
        elements_set.append(bar_set)
    return elements_set, max(song_counter.values())

def setup_page(parent) -> None:
    """
    Adds all the data to the stats page
    :return: None
    """
    # Update dates
    current_date = QDate.currentDate()
    parent.ui.played_songs_end.setDate(current_date)
    parent.ui.played_artists_end.setDate(current_date)
    parent.ui.occurrence_end.setDate(current_date)
    parent.ui.usage_times_end.setDate(current_date)

    history_data = parent.db_access.stats.get_history()

    sets, highest_val = get_n_most_played_songs(history_data, 10, parent)
    played_song_chart = BarChart("Played Songs", sets, highest_val)
    layout = parent.clear_field(parent.ui.played_songs_container, QVBoxLayout, amount_left = 0)
    layout.addWidget(played_song_chart)

    played_artists_chart = BarChart("Played Artists", sets, highest_val)
    layout = parent.clear_field(parent.ui.played_artists_container, QVBoxLayout, amount_left = 0)
    layout.addWidget(played_artists_chart)

    occurrence_chart = BarChart("Song Occurrences", sets, highest_val)
    layout = parent.clear_field(parent.ui.occurrence_container, QVBoxLayout, amount_left = 0)
    layout.addWidget(occurrence_chart)

    usage_times_chart = BarChart("Usage Times", sets, highest_val)
    layout = parent.clear_field(parent.ui.usage_times_container, QVBoxLayout, amount_left = 0)
    layout.addWidget(usage_times_chart)
