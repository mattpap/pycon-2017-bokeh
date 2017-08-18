import xml.etree.cElementTree as et
import pandas as pd
import shapefile as sf

trends = pd.read_csv("trends.csv", index_col=0) # index on state name
states = pd.read_csv("states.csv", index_col=1)

from bokeh.palettes import YlOrRd
bins = [0, 20, 40, 60, 80, 100]
colors = list(reversed(YlOrRd[len(bins) - 1]))
states["trend"] = pd.cut(trends["solar eclipse"], bins, labels=colors)

nan = float('NaN')

def parse_kml(kml):
    """
    <Polygon>
        <outerBoundaryIs>
            <LinearRing>
                <coordinates>...</coordinates>         <!-- lon,lat[,alt] -->
            </LinearRing>
        </outerBoundaryIs>
    </Polygon>
    """
    polygons = et.fromstring(kml).findall('.//outerBoundaryIs/LinearRing/coordinates')

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

states = states[(states.id != "AK") & (states.id != "HI")]

upath17 = sf.Reader("upath17")
eclipse, = upath17.shapes()

from bokeh.plotting import figure, show

p = figure(plot_width=1000, plot_height=600)

p.title.text = "Google Search Trends and the Path of Solar Eclipse, 21 August 2017"
p.title.align = "center"
p.title.text_font_size = "16pt"

from bokeh.models import MercatorTicker
p.xaxis.ticker = MercatorTicker(dimension="lon")
p.yaxis.ticker = MercatorTicker(dimension="lat")

p.grid.grid_line_color = None

from bokeh.models import ColorBar, LinearColorMapper

mapper = LinearColorMapper(palette=colors, low=0, high=100)
color_bar = ColorBar(color_mapper=mapper, orientation="horizontal", location="bottom_left",
    title="Popularity of \"solar eclipse\" search term", title_text_font_size="12pt", title_text_font_style="bold")
p.add_layout(color_bar)

state_xs = list(states.lons)
state_ys = list(states.lats)
trend = list(states.trend)

eclipse_x, eclipse_y = zip(*eclipse.points)

us = p.patches(state_xs, state_ys, fill_color=trend, line_color="white", line_width=1)
p.patch(eclipse_x, eclipse_y, fill_color="black", fill_alpha=0.7, line_color=None)

p.x_range.renderers = [us]
p.y_range.renderers = [us]

from bokeh.models import Label
path = Label(x=-77, y=31.4, angle=-37.5, angle_units="deg", text="Solar eclipse path of totality", text_font_size="8pt", text_color="silver")
p.add_layout(path)

#from bokeh.models import Label
#notes = Label(location="bottom_right", text="Google Trends, NASA Scientific Visualization Studio", text_font_size="8pt", text_color="silver")
#plot.add_layout(notes)

show(p)
print("DONE")