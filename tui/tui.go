package tui

import (
	"fmt"

	"github.com/charmbracelet/bubbles/key"
	tea "github.com/charmbracelet/bubbletea"
	gloss "github.com/charmbracelet/lipgloss"
)

type MainModel struct {
	List         PlaylistModel
	Player       PlayerModel
	ShortHelp    ShortHelpModel
	lastKeyPress string
	width        int
	height       int
}

func (m MainModel) Init() tea.Cmd {
	return m.Player.Init()
}

func (m MainModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch {
		case key.Matches(msg, mappings.Quit):
			return m, tea.Quit
		}
		m.lastKeyPress = msg.String()
	case tea.WindowSizeMsg:
		m.height = msg.Height
		m.width = msg.Width
		m.List.maxHeight = m.height - 4
		m.List.maxWidth = 40
		m.Player.maxWidth = 40
		m.ShortHelp.maxWidth = m.width - 40
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

	topHalf := gloss.JoinHorizontal(gloss.Top, m.List.View(), current)
	bottomHalf := gloss.JoinHorizontal(gloss.Top, m.Player.View(), m.ShortHelp.View())
	return gloss.JoinVertical(
		gloss.Left,
		topHalf,
		bottomHalf,
	)
}
