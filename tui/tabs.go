package tui

import (
	tea "github.com/charmbracelet/bubbletea"
	gloss "github.com/charmbracelet/lipgloss"
)

type TabsModel struct {
	maxWidth  int
	Titles    []string
	Contents  []string
	activeTab int
}

func (m TabsModel) Init() tea.Cmd {
	return nil
}

func (m TabsModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
	case tea.KeyMsg:
        switch msg.String() {
        case "1":
            m.activeTab = 0
        case "2":
            m.activeTab = 1
        case "3":
            m.activeTab = 2
        case "4":
            m.activeTab = 3
        case "5":
            m.activeTab = 4
        }
	}
	return m, nil
}

func (m TabsModel) View() string {
	titles := ""

	for i, title := range m.Titles {
		if m.activeTab == i {
			titles = gloss.JoinHorizontal(gloss.Left, titles, activeTitleStyle.Render(title))
		} else {
			titles = gloss.JoinHorizontal(gloss.Left, titles, titleStyle.Render(title))
		}
	}

	content := m.Contents[m.activeTab]

	return gloss.JoinVertical(gloss.Top, titles, content)
}
