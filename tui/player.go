package tui

import (
	"strings"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	gloss "github.com/charmbracelet/lipgloss"
)

type TickMsg time.Time

type PlayerModel struct {
	Tick     time.Duration
	Num      int
	maxWidth int
}

func doTick(tick time.Duration) tea.Cmd {
	return tea.Tick(tick, func(t time.Time) tea.Msg {
		return TickMsg(t)
	})
}

func (m PlayerModel) Init() tea.Cmd {
	// Start ticking.
	return doTick(m.Tick)
}

func (m PlayerModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg.(type) {
	case TickMsg:
		m.Num = (m.Num + 1) % (m.maxWidth - 2)
		// Return your Tick command again to loop.
		return m, doTick(m.Tick)
	}
	return m, nil
}

// leftmost char  ╺
// middle char    ━
// rightmost char ╸
func (m PlayerModel) View() string {
	if m.maxWidth > 0 {
		customBorder := gloss.Border{
			Top:         "─",
			Bottom:      "─",
			Left:        "│",
			Right:       "│",
			TopLeft:     "",
			TopRight:    "┤",
			BottomLeft:  "",
			BottomRight: "",
		}
		initial := []rune("╺" + strings.Repeat("━", m.maxWidth-5) + "╸")
		first := gloss.NewStyle().Foreground(gloss.Color("#FF0000")).Render(string(initial[:m.Num]))
		last := string(initial[m.Num:])
		return gloss.NewStyle().
			BorderStyle(customBorder).
			BorderForeground(gloss.Color("#999999")).
			BorderTop(true).
			BorderRight(true).
			Padding(1).
			Render("Song playing\n" + first + last)
	}
	return ""
}
