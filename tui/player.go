package tui

import (
	"strings"
	"time"

	tea "github.com/charmbracelet/bubbletea"
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
		initial := []rune("╺" + strings.Repeat("━", m.maxWidth-5) + "╸")
		first := progressBarCompleted.Render(string(initial[:m.Num]))
		last := string(initial[m.Num:])
		return playerStyling.Render("Song playing\n" + first + last)
	}
	return ""
}
