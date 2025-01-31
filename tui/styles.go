package tui

import (
	"github.com/charmbracelet/bubbles/help"
	gloss "github.com/charmbracelet/lipgloss"
)

var (
	// global stylings
	borderForeground = gloss.Color("#999999")

	// helper.go
	helperForePrimary   = gloss.Color("#DDD")
	helperForeSecondary = gloss.Color("#AAA")

	// player.go
	playerBorder = gloss.Border{
		Top:         "─",
		Bottom:      "─",
		Left:        "│",
		Right:       "│",
		TopLeft:     "",
		TopRight:    "┼",
		BottomLeft:  "",
		BottomRight: "",
	}
	playerStyling = gloss.NewStyle().
			BorderStyle(playerBorder).
			BorderForeground(borderForeground).
			BorderTop(true).
			BorderRight(true).
			Padding(1)
	progressBarCompleted = gloss.NewStyle().Foreground(gloss.Color("#FF0000"))

	// playlist.go
	// playlist items
	itemVPadding = 0
	itemHPadding = 1
	itemVMargin  = 1
	itemHMargin  = 0

	selectedBorderStyle = gloss.NewStyle().
				BorderLeft(true).
				BorderStyle(gloss.NormalBorder()).
				BorderForeground(gloss.Color("#773388")).
				Padding(itemVPadding, itemHPadding).
				Margin(itemVMargin, itemHMargin)
	selectedTitleStyle = gloss.NewStyle().Foreground(gloss.Color("#663399"))
	selectedTimeStyle  = gloss.NewStyle().Foreground(gloss.Color("#472471"))

	unselectedBorderStyle = gloss.NewStyle().
				BorderLeft(true).
				BorderStyle(gloss.HiddenBorder()).
				Padding(itemVPadding, itemHPadding).
				Margin(itemVMargin, itemHMargin)
	unselectedTitleStyle = gloss.NewStyle().Foreground(gloss.Color("#FFFFFF"))
	unselectedTimeStyle  = gloss.NewStyle().Foreground(gloss.Color("#AAAAAA"))

	// playlist styling
	playlistHMargin = 1
	playlistStyle   = gloss.NewStyle().
			Margin(0, playlistHMargin).
			BorderStyle(gloss.NormalBorder()).
			BorderForeground(borderForeground).
			BorderRight(true)
	additionStyle = gloss.NewStyle().MarginLeft(2)

	// shortHelp.go
	shortHelpStyling = gloss.NewStyle().
				Padding(1).
				BorderStyle(gloss.NormalBorder()).
				BorderTop(true).
				BorderForeground(borderForeground)

		// tabs.go
	activeColor      = gloss.Color("#F00")
	activeTitleStyle = gloss.NewStyle().Padding(1).MarginLeft(1).Foreground(activeColor)
	titleStyle       = gloss.NewStyle().Padding(1).MarginLeft(1)
)

// helper.go funcs
func NewStyledHelper(showAll bool) help.Model {
	helper := help.New()

	// Defining styles for help menus
	helper.Styles.FullKey = gloss.NewStyle().Inherit(helper.Styles.FullKey).Foreground(helperForePrimary)
	helper.Styles.ShortKey = gloss.NewStyle().Inherit(helper.Styles.ShortKey).Foreground(helperForePrimary)
	helper.Styles.FullDesc = gloss.NewStyle().Inherit(helper.Styles.FullDesc).Foreground(helperForeSecondary)
	helper.Styles.ShortDesc = gloss.NewStyle().Inherit(helper.Styles.ShortDesc).Foreground(helperForeSecondary)
	helper.Styles.FullSeparator = gloss.NewStyle().Inherit(helper.Styles.FullSeparator).Foreground(helperForeSecondary)
	helper.Styles.ShortSeparator = gloss.NewStyle().Inherit(helper.Styles.ShortSeparator).Foreground(helperForeSecondary)

	if showAll {
		helper.ShowAll = true
	}

	return helper
}

// playlist.go funcs
func getStyledAddition(text string, middlePoint int) string {
	return additionStyle.
		PaddingTop(middlePoint).
		PaddingBottom(middlePoint - 1).
		Render(text)
}

func getStyledPlaylist(text string, width int) string {
	return playlistStyle.Width(width - playlistHMargin*2).Render(text)
}

// shortHelp.go funcs
func getStyledShortHelp(text string, width int) string {
	return shortHelpStyling.Width(width).Render(text)
}
