import matplotlib.pyplot as plt
import matplotlib.dates as mdates
 
def line_chart(x, y, **options):
    fig, ax = plt.subplots(1)
 
    ax.plot(x, y, linewidth=4)
 
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())  
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))  
    plt.xticks(rotation=45)  
 
    ax.set(**options)
 
    fig.tight_layout()
    return fig