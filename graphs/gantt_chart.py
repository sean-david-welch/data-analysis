import plotly.figure_factory as ff
import plotly.io as pio

pio.renderers.default = "browser"


def create_gantt_data():
    tasks = [
        # Phase 1
        {"Task": "Project Setup", "Start": "2024-10-14", "Finish": "2024-10-18", "Phase": "Project Initialization", "Progress": 0},
        {"Task": "Requirements Analysis", "Start": "2024-10-14", "Finish": "2024-10-21", "Phase": "Project Initialization", "Progress": 0},

        # Phase 2
        {"Task": "Database Design", "Start": "2024-10-21", "Finish": "2024-10-25", "Phase": "Design", "Progress": 0},
        {"Task": "UI/UX Design", "Start": "2024-10-21", "Finish": "2024-10-28", "Phase": "Design", "Progress": 0},
        {"Task": "System Architecture Design", "Start": "2024-10-21", "Finish": "2024-10-28", "Phase": "Design", "Progress": 0},

        # Phase 3
        {"Task": "Backend Development - Core", "Start": "2024-10-28", "Finish": "2024-11-11", "Phase": "Development", "Progress": 0},
        {"Task": "Frontend Development - Basic", "Start": "2024-10-28", "Finish": "2024-11-11", "Phase": "Development", "Progress": 0},
        {"Task": "AI Integration", "Start": "2024-11-11", "Finish": "2024-11-25", "Phase": "Development", "Progress": 0},
        {"Task": "HTMX Implementation", "Start": "2024-11-11", "Finish": "2024-11-25", "Phase": "Development", "Progress": 0},

        # Phase 4
        {"Task": "Unit Testing", "Start": "2024-11-25", "Finish": "2024-12-02", "Phase": "Testing", "Progress": 0},
        {"Task": "Integration Testing", "Start": "2024-11-25", "Finish": "2024-12-02", "Phase": "Testing", "Progress": 0},
        {"Task": "User Testing", "Start": "2024-12-02", "Finish": "2024-12-09", "Phase": "Testing", "Progress": 0},

        # Phase 5
        {"Task": "AWS Setup", "Start": "2024-12-09", "Finish": "2024-12-13", "Phase": "Deployment", "Progress": 0},
        {"Task": "Deployment", "Start": "2024-12-13", "Finish": "2024-12-16", "Phase": "Deployment", "Progress": 0},
        {"Task": "Final Documentation", "Start": "2024-12-02", "Finish": "2024-12-18", "Phase": "Deployment", "Progress": 0}
    ]
    return tasks


def create_colours():
    return {
        "Project Initialization": "#3498db",
        "Design": "#9b59b6",
        "Development": "#e74c3c",
        "Testing": "#2ecc71",
        "Deployment": "#34495e"
    }


def create_gantt_chart(tasks):
    colors = create_colours()

    fig = ff.create_gantt(
        tasks,
        colors=colors,
        index_col='Phase',
        show_colorbar=True,
        group_tasks=True,
        showgrid_x=True,
        showgrid_y=True,
        bar_width=0.35,
        height=800
    )

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        title=dict(
            text='BudgetAI Development Timeline',
            font=dict(size=24, family="Arial", color="#2c3e50"),
            x=0.5,
            y=0.95
        ),
        xaxis=dict(
            title="Timeline",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(211, 211, 211, 0.5)',
            zeroline=False,
            showline=True,
            linewidth=2,
            linecolor='rgba(0,0,0,0.3)'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(211, 211, 211, 0.5)',
            zeroline=False,
            showline=True,
            linewidth=2,
            linecolor='rgba(0,0,0,0.3)'
        ),
        font=dict(
            family="Arial",
            size=14,
            color="#2c3e50"
        ),
        showlegend=True,
        legend=dict(
            title=dict(text="Project Phases"),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(0,0,0,0.2)',
            borderwidth=1,
            font=dict(size=12),
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.05
        ),
        margin=dict(l=250, r=250, t=100, b=100),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Arial"
        )
    )

    fig.update_xaxes(
        tickfont=dict(size=12),
        tickangle=45,
        tickformat="%Y-%m-%d",
        tickmode="auto",
        nticks=20,
        showline=True,
        linewidth=2,
        linecolor='rgba(0,0,0,0.3)'
    )

    fig.update_yaxes(
        tickfont=dict(size=12),
        showline=True,
        linewidth=2,
        linecolor='rgba(0,0,0,0.3)'
    )

    return fig


def main():
    tasks = create_gantt_data()
    fig = create_gantt_chart(tasks)
    fig.write_html("./graphs/project_gantt.html", include_plotlyjs=True, full_html=True)
    fig.show()


if __name__ == '__main__':
    main()
