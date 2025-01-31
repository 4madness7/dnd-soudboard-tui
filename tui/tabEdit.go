package tui

import (
	tea "github.com/charmbracelet/bubbletea"
)

type EditTabModel struct{}

func (m EditTabModel) Init() tea.Cmd {
	return nil
}

func (m EditTabModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	return m, nil
}

func (m EditTabModel) View() string {
	return "Edit"
}
