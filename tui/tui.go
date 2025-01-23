package tui

import (
	"fmt"

	tea "github.com/charmbracelet/bubbletea"
	gloss "github.com/charmbracelet/lipgloss"
)

type MainModel struct {
	width  int
	height int
	List   PlaylistModel
}

func (m MainModel) Init() tea.Cmd {
	return nil
}

func (m MainModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "ctrl+c", "esc", "q":
			return m, tea.Quit
		}
	case tea.WindowSizeMsg:
		m.height = msg.Height
		m.width = msg.Width
		m.List.maxHeight = m.height
		m.List.maxWidth = 40
	}

	var cmd tea.Cmd
	var model tea.Model
	model, cmd = m.List.Update(msg)
	m.List = model.(PlaylistModel)
	return m, cmd
}

func (m MainModel) View() string {
	current := gloss.NewStyle().
		Padding(3, 6).
		Render(fmt.Sprintf("Song selected: %v/%v\nW: %v | H: %v", m.List.Selected+1, len(m.List.List), m.width, m.height))
	return gloss.JoinHorizontal(gloss.Top, m.List.View(), current)
}
