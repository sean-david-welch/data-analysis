from graphviz import Digraph


def create_core_budget_usecase():
    dot = Digraph(comment='Core Budget Management')
    dot.attr(rankdir='LR')
    dot.attr(fontname='Arial')

    with dot.subgraph(name='cluster_0') as c:
        c.attr(label='Core Budget Management')
        c.attr(style='rounded')

        c.node('UC1', 'Create New Budget', shape='ellipse')
        c.node('UC2', 'Modify Budget\nLimits', shape='ellipse')
        c.node('UC3', 'Add Expense\nEntry', shape='ellipse')
        c.node('UC4', 'Categorize\nExpense', shape='ellipse')
        c.node('UC5', 'View Spending\nAnalytics', shape='ellipse')
        c.node('UC6', 'Generate\nReports', shape='ellipse')
        c.node('UC7', 'Set Budget\nAlerts', shape='ellipse')

        c.edge('UC3', 'UC4', 'includes', style='dashed')
        c.edge('UC3', 'UC5', 'includes', style='dashed')
        c.edge('UC5', 'UC6', 'extends', style='dashed')

    dot.node('User', 'User', shape='box', style='rounded')
    dot.node('AI', 'AI System', shape='component')

    for uc in ['UC1', 'UC2', 'UC3', 'UC5', 'UC6', 'UC7']:
        dot.edge('User', uc)

    dot.edge('AI', 'UC5')
    dot.edge('AI', 'UC6')

    return dot


def create_ai_features_usecase():
    dot = Digraph(comment='AI Features')
    dot.attr(rankdir='LR')
    dot.attr(fontname='Arial')

    with dot.subgraph(name='cluster_0') as c:
        c.attr(label='AI-Driven Features')
        c.attr(style='rounded')

        c.node('UC1', 'Get Personalized\nInsights', shape='ellipse')
        c.node('UC2', 'Receive Budget\nRecommendations', shape='ellipse')
        c.node('UC3', 'View Spending\nPredictions', shape='ellipse')
        c.node('UC4', 'Get Financial\nAdvice', shape='ellipse')
        c.node('UC5', 'Get Category\nRecommendations', shape='ellipse')
        c.node('UC6', 'Access AI\nGuidance', shape='ellipse')

        c.edge('UC1', 'UC2', 'includes', style='dashed')
        c.edge('UC1', 'UC3', 'includes', style='dashed')
        c.edge('UC4', 'UC6', 'includes', style='dashed')

    dot.node('User', 'User', shape='box', style='rounded')
    dot.node('ChatGPT', 'ChatGPT API', shape='component')

    for uc in ['UC1', 'UC4', 'UC6']:
        dot.edge('User', uc)

    for uc in ['UC1', 'UC2', 'UC3', 'UC4', 'UC5', 'UC6']:
        dot.edge('ChatGPT', uc)

    return dot


def create_user_management_usecase():
    dot = Digraph(comment='User Management')
    dot.attr(rankdir='LR')
    dot.attr(fontname='Arial')

    with dot.subgraph(name='cluster_0') as c:
        c.attr(label='User Management')
        c.attr(style='rounded')

        c.node('UC1', 'Register\nAccount', shape='ellipse')
        c.node('UC2', 'Login/\nAuthenticate', shape='ellipse')
        c.node('UC3', 'Manage\nProfile', shape='ellipse')
        c.node('UC4', 'Reset\nPassword', shape='ellipse')
        c.node('UC5', 'Configure\nNotifications', shape='ellipse')
        c.node('UC6', 'Manage Privacy\nSettings', shape='ellipse')

        c.edge('UC1', 'UC2', 'includes', style='dashed')
        c.edge('UC3', 'UC6', 'extends', style='dashed')

    dot.node('User', 'User', shape='box', style='rounded')
    dot.node('Admin', 'Administrator', shape='box', style='rounded')

    for uc in ['UC1', 'UC2', 'UC3', 'UC4', 'UC5', 'UC6']:
        dot.edge('User', uc)

    for uc in ['UC2', 'UC6']:
        dot.edge('Admin', uc)

    return dot


if __name__ == "__main__":
    diagrams = {
        'core_budget': create_core_budget_usecase(),
        'ai_features': create_ai_features_usecase(),
        'user_management': create_user_management_usecase(),
    }

    for name, diagram in diagrams.items():
        diagram.render(f'./graphs/output/{name}_usecase', format='png', cleanup=True)
