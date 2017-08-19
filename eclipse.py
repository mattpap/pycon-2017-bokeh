# Based on https://www.reddit.com/r/dataisbeautiful/comments/6qnkg0/google_search_interest_follows_the_path_of_the/

#%%
from bokeh.io import output_notebook
output_notebook()

import shapefile as sf
upath17 = sf.Reader("upath17")
(totality_path,) = upath17.shapes()

import xml.etree.cElementTree as et
import pandas as pd

trends = pd.read_csv("trends.csv", index_col=0) # index on state name
states = pd.read_csv("states.csv", index_col=1)

states = states[(states.id != "AK") & (states.id != "HI")]

def parse_kml(kml):
    """
    <Polygon>
        <outerBoundaryIs>
            <LinearRing>
                <coordinates>...</coordinates>
                <!-- lon,lat[,alt] -->
            </LinearRing>
        </outerBoundaryIs>
    </Polygon>
    """
    nan = float('NaN')

    xml = et.fromstring(kml)
    polygons = xml.findall('.//outerBoundaryIs/LinearRing/coordinates')

    lons = []
    lats = []
    for i, polygon in enumerate(polygons):
        if i > 0:
            lons.append(nan)
            lats.append(nan)
        coords = (c.split(',')[:2] for c in polygon.text.split())
        lon, lat = list(zip(*[(float(lon), float(lat)) for lon, lat in coords]))
        lons.extend(lon)
        lats.extend(lat)
    return lons, lats

coords = states.geometry.map(parse_kml)
states["lons"] = coords.map(lambda row: row[0])
states["lats"] = coords.map(lambda row: row[1])

from bokeh.plotting import figure, show

p = figure(plot_width=1000, plot_height=600)

p.title.text = "Google Search Trends and the Path of Solar Eclipse, 21 August 2017"
p.title.align = "center"
p.title.text_font_size = "16pt"

from bokeh.palettes import YlOrRd
bins = [0, 20, 40, 60, 80, 100]
colors = list(reversed(YlOrRd[len(bins) - 1]))
states["trend"] = trends["solar eclipse"]
states["trend_binned"] = pd.cut(states.trend, bins, labels=colors)

state_xs = list(states.lons)
state_ys = list(states.lats)
trend = list(states.trend_binned)

eclipse_x, eclipse_y = zip(*totality_path.points)

from bokeh.models import ColumnDataSource
source = ColumnDataSource(data=dict(trend=states.trend))

from bokeh.models import LinearColorMapper
mapper = LinearColorMapper(palette=colors, low=0, high=100)

map = p.patches(state_xs, state_ys, fill_color=trend, line_color="white", line_width=1)
#map = p.patches(state_xs, state_ys, fill_color=dict(field="trend", transform=mapper), source=source, line_color="white", line_width=1)
p.patch(eclipse_x, eclipse_y, fill_color="black", fill_alpha=0.7, line_color=None)

p.x_range.renderers = [map]
p.y_range.renderers = [map]

p.grid.grid_line_color = None

from bokeh.models import Label
path = Label(x=-77, y=31.4, angle=-36.5, angle_units="deg", text="Solar eclipse path of totality", text_font_size="8pt", text_color="silver")
p.add_layout(path)

from bokeh.models import ColorBar

color_bar = ColorBar(color_mapper=mapper, orientation="horizontal", location="bottom_left",
    title="Popularity of \"solar eclipse\" search term", title_text_font_size="12pt", title_text_font_style="bold",
    background_fill_alpha=0)
p.add_layout(color_bar)

from bokeh.models import Label, Range1d
p.extra_x_ranges["x_screen"] = Range1d(0, 1, bounds="auto")
p.extra_y_ranges["y_screen"] = Range1d(0, 1, bounds="auto")
notes = Label(
    x=0, y=0, x_offset=40, y_offset=20,
    x_range_name="x_screen",
    y_range_name="y_screen",
    text="Source: Google Trends, NASA Scientific Visualization Studio",
    level="overlay",
    text_font_size="8pt",
    text_color="gray")
p.add_layout(notes)

show(p)
