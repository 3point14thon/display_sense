from scipy import stats
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio

def get_pdf(x_range, store_data):
    """ The function will return the pdf for a given beta distribution.
    
    Args:
        x_range: Array of x values for the plot.
        store_data: Array of values for a store. A value of 1 represents a positive customer
                    result while an value of 0 represents a negative result. 
                    
    Returns:
        A numpy array representing the PDF for the given beta distribution.
    """
    alpha = sum(store_data)
    beta = len(store_data) - alpha
    return stats.beta(a=alpha, b=beta).pdf(x_range)

def generate_plotly_area_fig(x_range, x_min, x_max, y_min, y_max, pdf_a, pdf_b, n_customers):
    """ The function will return a Plotly figure. 
    
    Args:
        x_range: Array of x values for the plot.
        x_min: Lower limit to display for the x-axis
        x_max: Upper limit to display for the x-axis
        y_min: Lower limit to display for the x-axis
        y_max: Upper limit to display for the x-axis
        pdf_a: The PDF generated by the data from store A
        pdf_b: The PDF generated by the data from store B 
                    
    Returns:
        A Plotly figure
    """
    trace1 = go.Scatter(
        x=x_range,
        y=pdf_a,
        name='Store A',
        fill='tozeroy',
        line = dict(
          color = '#006b3c'
            )
        )

    trace2 = go.Scatter(
        x=x_range,
        y=pdf_b,
        name='Store B',
        fill='tozeroy',
        line = dict(
            color = '#c41e3a'
            )
        )

    layout = go.Layout(
        xaxis=dict(
            title='Conversion Rate',
            range=[x_min, x_max]
        ),
        yaxis=dict(
            range=[y_min, y_max]
        ),
        title=f'Conversion Rate Posterior Distributions After {n_customers} Users'
    )

    data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)
    return fig

# n_customers = [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000]
def generate_plotly_frames(data_store_a, data_store_b, n_customers):
    """ The function will return a list of figures for Plotly to animate.
    
    Args:
        data_store_a: An array of zeros and ones, where ones represent a "success" at a given store/display.
                      In this case, a success could be defined as a person deciding to walk into the store. 
        data_store_b: An array at zeros and ones like data_store_a but for a different store/display.
        n_customers:  A list with the number of customers 
                    
    Returns:
        A list of plotly figures that can be used to plot sequential images
    """
    frames = []
    for n in n_customers:
        x_range = np.arange(0, 1.001, 0.001)
        pdf_a = get_pdf(x_range, data_store_a[:n])
        pdf_b = get_pdf(x_range, data_store_b[:n])
        fig = generate_plotly_area_fig(x_range, 0, .1, 0, 125, pdf_a, pdf_b, n)
        frames.append(fig)
        
    return frames

def export_frame_images(frames, base_fig_name):
    """ The function will return a list of figures for Plotly to animate.
    
    Args:
        frames: A list of Plotly figures
        base_fig_name: The base name that you want the output files saved as. If the base name is  "flagshipStore" then 
                       the files will be output as flagshipStore0.png, flagshipStore1.png, etc. 
                    
    Returns:
        This function exports a sequence of PNG files that can then be used to turn into a gif. 
    """
    for i, frame in enumerate(frames):
        pio.write_image(frame, base_fig_name + str(i) + '.png')