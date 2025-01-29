package tui

import (
	"github.com/charmbracelet/bubbles/help"
	tea "github.com/charmbracelet/bubbletea"
)

type ShortHelpModel struct {
	Helper   help.Model
	maxWidth int
}

func (m ShortHelpModel) Init() tea.Cmd {
	return nil
}

func (m ShortHelpModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	return m, nil
}

func (m ShortHelpModel) View() string {
	return getStyledShortHelp(m.Helper.View(mappings), m.maxWidth)
}
