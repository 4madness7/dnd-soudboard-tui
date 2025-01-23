package main

import (
	"4madness7/dnd-soundboard-tui/tui"
	"fmt"
	"os"

	tea "github.com/charmbracelet/bubbletea"
	// gloss "github.com/charmbracelet/lipgloss"
)

func main() {
	listItems := []tui.Item{
		{Title: "Song #1", Timer: "23:45"},
		{Title: "Song #2", Timer: "45"},
		{Title: "Song #3", Timer: "2:23:45"},
		{Title: "Song #4", Timer: "3:45"},
		{Title: "Song #5", Timer: "4:50"},
		{Title: "Song #6", Timer: "5:23:45"},
		{Title: "Song #7", Timer: "6:23:45"},
		{Title: "Song #8", Timer: "7:23:45"},
		{Title: "Song #9", Timer: "8:23:45"},
		{Title: "Song #10", Timer: "23:45"},
		{Title: "Song #11", Timer: "45"},
		{Title: "Song #12", Timer: "2:23:45"},
		{Title: "Song #13", Timer: "3:45"},
		{Title: "Song #14", Timer: "3:45"},
		{Title: "Song #15", Timer: "3:45"},
		{Title: "Song #16", Timer: "3:45"},
		{Title: "Song #17", Timer: "3:45"},
		{Title: "Song #18", Timer: "3:45"},
	}

	m := tui.MainModel{
		List: tui.PlaylistModel{
			List:     listItems,
			Selected: 0,
		},
	}

	p := tea.NewProgram(m, tea.WithAltScreen())

	if _, err := p.Run(); err != nil {
		fmt.Println("Error while running program:", err)
		os.Exit(1)
	}
}
