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
	Tabs         TabsModel
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
		m.lastKeyPress = msg.String()
		switch {
		case key.Matches(msg, mappings.Quit):
			return m, tea.Quit
		case key.Matches(msg, mappings.Playlists.Binding),
			key.Matches(msg, mappings.Soundboard.Binding),
			key.Matches(msg, mappings.Insert.Binding),
			key.Matches(msg, mappings.Edit.Binding),
			key.Matches(msg, mappings.Helper.Binding):

			var cmd tea.Cmd
			var model tea.Model
			model, cmd = m.Tabs.Update(msg)
			m.Tabs = model.(TabsModel)
			return m, cmd
		}
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

	test := gloss.JoinVertical(gloss.Top, m.Tabs.View(), current)
	topHalf := gloss.JoinHorizontal(gloss.Top, m.List.View(), test)
	bottomHalf := gloss.JoinHorizontal(gloss.Top, m.Player.View(), m.ShortHelp.View())
	return gloss.JoinVertical(
		gloss.Left,
		topHalf,
		bottomHalf,
	)
}
