package tui

import (
	"github.com/charmbracelet/bubbles/help"
	tea "github.com/charmbracelet/bubbletea"
	gloss "github.com/charmbracelet/lipgloss"
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
	return gloss.NewStyle().
		Width(m.maxWidth).
		Padding(1).
		BorderStyle(gloss.NormalBorder()).
		BorderTop(true).
		BorderForeground(gloss.Color("#999999")).
		Render(m.Helper.View(mappings))
}
