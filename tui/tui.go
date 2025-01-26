package tui

import (
	"fmt"

	tea "github.com/charmbracelet/bubbletea"
	gloss "github.com/charmbracelet/lipgloss"
)

type MainModel struct {
	width        int
	height       int
	List         PlaylistModel
	Player       PlayerModel
	lastKeyPress string
}

func (m MainModel) Init() tea.Cmd {
	return m.Player.Init()
}

func (m MainModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "ctrl+c", "esc", "q":
			return m, tea.Quit
		}
		m.lastKeyPress = msg.String()
	case tea.WindowSizeMsg:
		m.height = msg.Height
		m.width = msg.Width
		m.List.maxHeight = m.height - 4
		m.List.maxWidth = 40
		m.Player.maxWidth = 40
	case TickMsg:
		var cmd tea.Cmd
		var model tea.Model
		model, cmd = m.Player.Update(msg)
		m.Player = model.(PlayerModel)
		return m, cmd
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
		Render(
			fmt.Sprintf(
				"W: %v | H: %v\nSelected: %v | Start: %v | Stop: %v\nLast key pressed: %v",
				m.width,
				m.height,
				m.List.selected,
				m.List.renderStart,
				m.List.renderStop,
				m.lastKeyPress,
			),
		)
	return gloss.JoinHorizontal(
		gloss.Top,
		gloss.JoinVertical(gloss.Left, m.List.View(), m.Player.View()),
		current,
	)
}
