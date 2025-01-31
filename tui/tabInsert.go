package tui

import (
	tea "github.com/charmbracelet/bubbletea"
)

type InsertTabModel struct{}

func (m InsertTabModel) Init() tea.Cmd {
	return nil
}

func (m InsertTabModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	return m, nil
}

func (m InsertTabModel) View() string {
	return "Insert"
}
