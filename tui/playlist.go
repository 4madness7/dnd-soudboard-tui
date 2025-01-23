package tui

import (
	"fmt"
	"strings"

	tea "github.com/charmbracelet/bubbletea"
	gloss "github.com/charmbracelet/lipgloss"
)

type Item struct {
	Title, Timer string
}

func (i Item) GetTime() string {
	t := strings.Split(i.Timer, ":")
	switch len(t) {
	case 1:
		return fmt.Sprintf("%vs", t[0])
	case 2:
		return fmt.Sprintf("%vm %vs", t[0], t[1])
	default:
		return fmt.Sprintf("%vh %vm %vs", t[0], t[1], t[2])
	}
}

func (i Item) GetStyledOutput(isSelected bool) string {
	vPadding := 0
	hPadding := 1
	vMargin := 1
	hMargin := 0

	if isSelected {
		selectedBorderStyle := gloss.NewStyle().
			BorderLeft(true).
			BorderStyle(gloss.NormalBorder()).
			BorderForeground(gloss.Color("#773388")).
			Padding(vPadding, hPadding).
			Margin(vMargin, hMargin)
		selectedTitleStyle := gloss.NewStyle().Foreground(gloss.Color("#663399"))
		selectedTimeStyle := gloss.NewStyle().Foreground(gloss.Color("#472471"))
		styledText := fmt.Sprintf("%s\n%s", selectedTitleStyle.Render(i.Title), selectedTimeStyle.Render(i.GetTime()))
		return selectedBorderStyle.Render(styledText)
	}

	unselectedBorderStyle := gloss.NewStyle().
		BorderLeft(true).
		BorderStyle(gloss.HiddenBorder()).
		Padding(vPadding, hPadding).
		Margin(vMargin, hMargin)

	unselectedTitleStyle := gloss.NewStyle().Foreground(gloss.Color("#FFFFFF"))
	unselectedTimeStyle := gloss.NewStyle().Foreground(gloss.Color("#AAAAAA"))
	styledText := fmt.Sprintf("%s\n%s", unselectedTitleStyle.Render(i.Title), unselectedTimeStyle.Render(i.GetTime()))
	return unselectedBorderStyle.Render(styledText)
}

type PlaylistModel struct {
	List        []Item
	maxHeight   int
	maxWidth    int
	Selected    int
	canRender   int
	renderStart int
	renderStop  int
}

func (m PlaylistModel) Init() tea.Cmd {
	return nil
}

func (m PlaylistModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "j", "down":
			m.Selected = (m.Selected + 1) % len(m.List)
			if m.Selected > m.renderStop {
				m.renderStart++
				m.renderStop++
			}
			if m.Selected == 0 && m.renderStart != 0 {
				m.renderStart = m.Selected
				if m.canRender >= len(m.List) {
					m.renderStop = len(m.List) - 1
				} else {
					m.renderStop = m.renderStart + m.canRender - 1
				}
			}
		case "k", "up":
			m.Selected--
			if m.Selected < 0 {
				m.Selected = len(m.List) - 1
			}
			if m.Selected < m.renderStart {
				m.renderStart--
				m.renderStop--
			}
			if m.Selected == len(m.List)-1 && m.renderStop != len(m.List)-1 {
				m.renderStop = m.Selected
				if m.canRender >= len(m.List) {
					m.renderStart = 0
				} else {
					m.renderStart = m.renderStop - m.canRender + 1
				}
			}
		}
	case tea.WindowSizeMsg:
		m.canRender = m.maxHeight/3 - 1

		m.renderStart = m.Selected
		if m.canRender >= len(m.List) {
			m.renderStop = len(m.List) - 1
		} else {
			m.renderStop = m.renderStart + m.canRender - 1
		}
	}
	return m, nil
}

func (m PlaylistModel) View() string {
	output := ""

	for i := m.renderStart; i <= m.renderStop; i++ {
		output += m.List[i].GetStyledOutput(i == m.Selected)
	}

	if diff := m.maxHeight - len(strings.Split(output, "\n")); diff > 0 {
		toAdd := ""
		for i := 0; i < diff; i++ {
			toAdd += "\n"
		}
		output += toAdd
	}

	return gloss.NewStyle().
		Margin(0, 2).
		BorderStyle(gloss.NormalBorder()).
		BorderForeground(gloss.Color("#999999")).
		BorderRight(true).
		Render(output)
}
