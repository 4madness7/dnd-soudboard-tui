package tui

import (
	tea "github.com/charmbracelet/bubbletea"
)

type SoundboardTabModel struct{}

func (m SoundboardTabModel) Init() tea.Cmd {
	return nil
}

func (m SoundboardTabModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	return m, nil
}

func (m SoundboardTabModel) View() string {
	return "Soundboard"
}
