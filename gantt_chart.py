import plotly.figure_factory as ff
import plotly.io as pio
# Configure plotly to use a different renderer
pio.renderers.default = "browser"


def create_gantt_data():
    # Format: Task, Start Date, End Date, Duration (days)
    tasks = [
        # Phase 1: Project Setup & Requirements
        ["Project Setup", "2024-10-14", "2024-10-18", 5],
        ["Requirements Analysis", "2024-10-14", "2024-10-21", 8],
        # Phase 2: Design & Architecture
        ["Database Design", "2024-10-21", "2024-10-25", 5],
        ["UI/UX Design", "2024-10-21", "2024-10-28", 8],
        ["System Architecture Design", "2024-10-21", "2024-10-28", 8],
        # Phase 3: Development
        ["Backend Development - Core", "2024-10-28", "2024-11-11", 15],
        ["Frontend Development - Basic", "2024-10-28", "2024-11-11", 15],
        ["AI Integration", "2024-11-11", "2024-11-25", 14],
        ["HTMX Implementation", "2024-11-11", "2024-11-25", 14],
        # Phase 4: Testing & Integration
        ["Unit Testing", "2024-11-25", "2024-12-02", 7],
        ["Integration Testing", "2024-11-25", "2024-12-02", 7],
        ["User Testing", "2024-12-02", "2024-12-09", 7],
        # Phase 5: Deployment & Documentation
        ["AWS Setup", "2024-12-09", "2024-12-13", 5],
        ["Deployment", "2024-12-13", "2024-12-16", 4],
        ["Final Documentation", "2024-12-02", "2024-12-18", 17]
    ]

    df = []
    for task in tasks:
        df.append(dict(Task=task[0],
                       Start=task[1],
                       Finish=task[2],
                       Duration=task[3]))
    return df


def create_gantt_chart(df):
    colors = {
        'Project Setup': 'rgb(46, 137, 205)',
        'Requirements Analysis': 'rgb(46, 137, 205)',
        'Database Design': 'rgb(114, 44, 121)',
        'UI/UX Design': 'rgb(114, 44, 121)',
        'System Architecture Design': 'rgb(114, 44, 121)',
        'Backend Development - Core': 'rgb(198, 47, 105)',
        'Frontend Development - Basic': 'rgb(198, 47, 105)',
        'AI Integration': 'rgb(198, 47, 105)',
        'HTMX Implementation': 'rgb(198, 47, 105)',
        'Unit Testing': 'rgb(58, 149, 136)',
        'Integration Testing': 'rgb(58, 149, 136)',
        'User Testing': 'rgb(58, 149, 136)',
        'AWS Setup': 'rgb(107, 127, 135)',
        'Deployment': 'rgb(107, 127, 135)',
        'Final Documentation': 'rgb(107, 127, 135)'
    }

    fig = ff.create_gantt(df,
                          colors=colors,
                          index_col='Task',
                          show_colorbar=True,
                          group_tasks=True,
                          showgrid_x=True,
                          showgrid_y=True,
                          bar_width=0.3)

    # Update layout with improved readability
    fig.update_layout(
        title=dict(
            text='Personal Budgeting Tool Development Timeline',
            font=dict(size=24),
            x=0.5,
            y=0.95
        ),
        xaxis_title=dict(
            text='Date',
            font=dict(size=16)
        ),
        height=800,
        font=dict(size=14),
        showlegend=True,
        legend=dict(
            font=dict(size=14),
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.05
        ),
        margin=dict(l=250, r=250, t=100, b=100)
    )

    # Update axes for better readability
    fig.update_xaxes(
        tickfont=dict(size=14),
        tickangle=45
    )

    fig.update_yaxes(
        tickfont=dict(size=14)
    )

    # Update text style for all traces
    for trace in fig.data:
        trace.update(
            textfont=dict(size=14, color='black'),
            textposition='middle center'
        )

    return fig


# Generate the data and create the chart
df = create_gantt_data()
fig = create_gantt_chart(df)

# Save as HTML
fig.write_html("project_gantt.html")

# This will open the plot in your default browser
fig.show()

print("The Gantt chart has been saved as 'project_gantt.html' and opened in your browser.")
print("You can use your browser's print functionality (CMD/CTRL + P) to save it as a PDF.")
print("Tips for saving as PDF from browser:")
print("1. Set the orientation to Landscape")
print("2. Enable 'Background graphics' in print settings")
print("3. Choose 'Save as PDF' as the destination")
