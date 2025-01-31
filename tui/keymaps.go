package tui

import "github.com/charmbracelet/bubbles/key"

type tabBinding struct {
	key.Binding
	index int
}

type keyMap struct {
	Up         key.Binding
	Down       key.Binding
	Quit       key.Binding
	Playlists  tabBinding
	Soundboard tabBinding
	Insert     tabBinding
	Edit       tabBinding
	Helper     tabBinding
}

var mappings = keyMap{
	Up: key.NewBinding(
		key.WithKeys("up", "k"),
		key.WithHelp("up/k", "Move up"),
	),
	Down: key.NewBinding(
		key.WithKeys("down", "j"),
		key.WithHelp("down/j", "Move down"),
	),
	Quit: key.NewBinding(
		key.WithKeys("q", "ctrl+c", "esc"),
		key.WithHelp("q/crtl+c/esc", "Quit"),
	),
	Playlists: tabBinding{
		Binding: key.NewBinding(
			key.WithKeys("ctrl+p"),
			key.WithHelp("ctrl+p", "'Playlists' tab"),
		),
		index: 0,
	},
	Soundboard: tabBinding{
		Binding: key.NewBinding(
			key.WithKeys("ctrl+s"),
			key.WithHelp("ctrl+s", "'Soundboard' tab"),
		),
		index: 1,
	},
	Insert: tabBinding{
		Binding: key.NewBinding(
			key.WithKeys("ctrl+n"),
			key.WithHelp("ctrl+n", "'Insert' tab"),
		),
		index: 2,
	},
	Edit: tabBinding{
		Binding: key.NewBinding(
			key.WithKeys("ctrl+e"),
			key.WithHelp("ctrl+e", "'Edit' tab"),
		),
		index: 3,
	},
	Helper: tabBinding{
		Binding: key.NewBinding(
			key.WithKeys("?"),
			key.WithHelp("?", "'Help' tab"),
		),
		index: 4,
	},
}

// ShortHelp returns keybindings to be shown in the mini help view. It's part
// of the key.Map interface.
func (k keyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.Up,
		k.Down,
		k.Quit,
		k.Playlists.Binding,
		k.Soundboard.Binding,
		k.Insert.Binding,
		k.Edit.Binding,
		k.Helper.Binding,
	}
}

// FullHelp returns keybindings for the expanded help view. It's part of the
// key.Map interface.
func (k keyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.Up, k.Down}, // first column
		{k.Quit},       // second column
	}
}
