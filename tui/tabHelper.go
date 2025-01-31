package tui

import (
	"github.com/charmbracelet/bubbles/help"
	tea "github.com/charmbracelet/bubbletea"
)

type HelperTabModel struct {
	Helper help.Model
}

func (m HelperTabModel) Init() tea.Cmd {
	return nil
}

func (m HelperTabModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	return m, nil
}

func (m HelperTabModel) View() string {
	return m.Helper.View(mappings)
}
