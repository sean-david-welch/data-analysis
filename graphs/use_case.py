from graphviz import Digraph


def create_budget_tool_usecase():
    """
    Creates a comprehensive use case diagram for an AI-driven Personal Budgeting Tool
    using graphviz. The diagram includes core budgeting features, AI capabilities,
    and user management functionality.

    Returns:
        Digraph: A graphviz diagram object
    """
    # Initialize diagram with custom settings
    dot = Digraph(comment='AI Budget Tool Use Case Diagram')
    dot.attr(rankdir='LR')
    dot.attr(fontname='Arial')

    # Define system boundary
    with dot.subgraph(name='cluster_0') as c:
        c.attr(label='AI Personal Budget Tool System')
        c.attr(style='rounded')

        # Core Budget Management Use Cases
        c.node('UC1', 'Create/Modify Budget\nLimits', shape='ellipse')
        c.node('UC2', 'Track Expenses', shape='ellipse')
        c.node('UC3', 'Categorize\nTransactions', shape='ellipse')
        c.node('UC4', 'View Spending\nAnalytics', shape='ellipse')

        # AI-Driven Features
        c.node('UC5', 'Generate AI\nInsights', shape='ellipse')
        c.node('UC6', 'Get Budget\nRecommendations', shape='ellipse')
        c.node('UC7', 'View Spending\nPredictions', shape='ellipse')
        c.node('UC8', 'Receive Financial\nAdvice', shape='ellipse')

        # Account & Data Management
        c.node('UC9', 'Manage Profile', shape='ellipse')
        c.node('UC10', 'Authenticate', shape='ellipse')
        c.node('UC11', 'Export Financial\nData', shape='ellipse')
        c.node('UC12', 'Set Notification\nPreferences', shape='ellipse')

        # Security Features
        c.node('UC13', 'Manage Data\nPrivacy Settings', shape='ellipse')

        # Include relationships (core functionality)
        c.edge('UC2', 'UC3', 'includes', style='dashed')
        c.edge('UC2', 'UC4', 'includes', style='dashed')

        # Include relationships (AI features)
        c.edge('UC4', 'UC5', 'includes', style='dashed')
        c.edge('UC5', 'UC6', 'includes', style='dashed')
        c.edge('UC5', 'UC7', 'includes', style='dashed')
        c.edge('UC5', 'UC8', 'includes', style='dashed')

        # Extend relationships
        c.edge('UC13', 'UC9', 'extends', style='dashed')
        c.edge('UC11', 'UC4', 'extends', style='dashed')

    # Define actors with custom shapes
    dot.node('User', 'Regular User', shape='box', style='rounded')
    dot.node('Admin', 'Administrator', shape='box', style='rounded')
    dot.node('AI', 'ChatGPT API', shape='component')
    dot.node('NotifSystem', 'Notification\nSystem', shape='component')

    # User relationships
    user_cases = ['UC1', 'UC2', 'UC4', 'UC8', 'UC9', 'UC10', 'UC11', 'UC12', 'UC13']
    for uc in user_cases:
        dot.edge('User', uc)

    # Admin relationships
    admin_cases = ['UC9', 'UC10', 'UC13']
    for uc in admin_cases:
        dot.edge('Admin', uc)

    # AI system relationships
    ai_cases = ['UC5', 'UC6', 'UC7', 'UC8']
    for uc in ai_cases:
        dot.edge('AI', uc)

    # Notification system relationships
    dot.edge('NotifSystem', 'UC12')

    return dot


def generate_diagrams():
    """
    Generates and saves the use case diagram in multiple formats
    """
    diagram = create_budget_tool_usecase()

    formats = ['png', 'svg', 'pdf']
    for fmt in formats:
        output_path = './graphs/output/budget_tool_usecase'
        diagram.render(output_path, format=fmt, cleanup=True)


if __name__ == "__main__":
    generate_diagrams()
