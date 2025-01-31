package tui

import (
	"github.com/charmbracelet/bubbles/key"
	tea "github.com/charmbracelet/bubbletea"
	gloss "github.com/charmbracelet/lipgloss"
)

type TabsModel struct {
	PlaylistsTab  PlaylistsTabModel
	SoundboardTab SoundboardTabModel
	InsertTab     InsertTabModel
	EditTab       EditTabModel
	HelperTab     HelperTabModel
	ActiveView    tea.Model
	Titles        []string
	maxWidth      int
	activeTab     int
}

func (m TabsModel) Init() tea.Cmd {
	return nil
}

func (m TabsModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch {
		case key.Matches(msg, mappings.Playlists.Binding):
			m.activeTab = mappings.Playlists.index
			m.ActiveView = m.PlaylistsTab
		case key.Matches(msg, mappings.Soundboard.Binding):
			m.activeTab = mappings.Soundboard.index
			m.ActiveView = m.SoundboardTab
		case key.Matches(msg, mappings.Insert.Binding):
			m.activeTab = mappings.Insert.index
			m.ActiveView = m.InsertTab
		case key.Matches(msg, mappings.Edit.Binding):
			m.activeTab = mappings.Edit.index
			m.ActiveView = m.EditTab
		case key.Matches(msg, mappings.Helper.Binding):
			m.activeTab = mappings.Helper.index
			m.ActiveView = m.HelperTab
		}
	}
	return m, nil
}

func (m TabsModel) View() string {
	titles := ""

	for i, title := range m.Titles {
		if m.activeTab == i {
			titles = gloss.JoinHorizontal(gloss.Left, titles, activeTitleStyle.Render(title))
		} else {
			titles = gloss.JoinHorizontal(gloss.Left, titles, titleStyle.Render(title))
		}
	}

	content := m.ActiveView.View()

	return gloss.JoinVertical(gloss.Top, titles, content)
}
