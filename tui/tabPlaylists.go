package tui

import (
	tea "github.com/charmbracelet/bubbletea"
)

type PlaylistsTabModel struct{}

func (m PlaylistsTabModel) Init() tea.Cmd {
	return nil
}

func (m PlaylistsTabModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	return m, nil
}

func (m PlaylistsTabModel) View() string {
	return "Playlists"
}
