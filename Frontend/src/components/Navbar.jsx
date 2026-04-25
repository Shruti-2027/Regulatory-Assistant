import { useEffect, useRef, useState } from 'react'
import RegulatoryLogo from './RegulatoryLogo'

const NAV_LINKS = [{ label: 'Workflow', href: '#document-review' }]

export default function Navbar({ theme, onToggleTheme }) {
  const [menuOpen, setMenuOpen] = useState(false)
  const [profileOpen, setProfileOpen] = useState(false)
  const profileRef = useRef(null)

  useEffect(() => {
    function handleClickOutside(e) {
      if (profileRef.current && !profileRef.current.contains(e.target)) {
        setProfileOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  useEffect(() => {
    if (!menuOpen) return
    function onEsc(e) {
      if (e.key === 'Escape') setMenuOpen(false)
    }
    document.addEventListener('keydown', onEsc)
    return () => document.removeEventListener('keydown', onEsc)
  }, [menuOpen])

  const isDark = theme === 'dark'

  return (
    <header className="navbar">
      <div className="navbar__inner">
        <a href="#document-review" className="navbar__brand" onClick={() => setMenuOpen(false)}>
          <RegulatoryLogo className="navbar__logo" />
          <span className="navbar__name">Regulatory Assistant</span>
        </a>

        <nav
          id="primary-nav"
          className={`navbar__nav ${menuOpen ? 'navbar__nav--open' : ''}`}
          aria-label="Primary"
        >
          <ul className="navbar__links">
            {NAV_LINKS.map(({ label, href }) => (
              <li key={href}>
                <a href={href} className="navbar__link" onClick={() => setMenuOpen(false)}>
                  {label}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        <div className="navbar__actions">
          <button
            type="button"
            className="theme-toggle"
            onClick={onToggleTheme}
            aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
            title={isDark ? 'Light mode' : 'Dark mode'}
          >
            <span className="theme-toggle__track" aria-hidden>
              <span className="theme-toggle__thumb" />
            </span>
            <span className="theme-toggle__icon theme-toggle__icon--sun" aria-hidden>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 18a6 6 0 1 1 0-12 6 6 0 0 1 0 12Zm0-2a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM11 1h2v3h-2V1Zm0 19h2v3h-2v-3ZM3.515 4.929l1.414-1.414L7.05 5.636 5.636 7.05 3.515 4.93ZM16.95 18.364l1.414-1.414 2.121 2.121-1.414 1.414-2.121-2.121Zm2.121-14.85 1.414 1.414-2.121 2.121-1.414-1.414 2.121-2.121ZM5.636 16.95l1.414 1.414-2.121 2.121-1.414-1.414 2.121-2.121ZM23 11v2h-3v-2h3ZM4 11v2H1v-2h3Z" />
              </svg>
            </span>
            <span className="theme-toggle__icon theme-toggle__icon--moon" aria-hidden>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                <path d="M10 7a7 7 0 0 0 12 4.9v.1a7 7 0 1 1-12-5Z" />
              </svg>
            </span>
          </button>

          <div className="navbar__profile-wrap" ref={profileRef}>
            <button
              type="button"
              className="navbar__profile-btn"
              aria-expanded={profileOpen}
              aria-haspopup="dialog"
              onClick={() => setProfileOpen((v) => !v)}
            >
              <span className="navbar__avatar" aria-hidden>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
              </span>
            </button>
            {profileOpen && (
              <div className="navbar__dropdown navbar__dropdown--profile" role="dialog" aria-label="Account menu">
                <div className="navbar__profile-header">
                  <p className="navbar__profile-name">Regulatory Analyst</p>
                  <p className="navbar__profile-role">Life Sciences Compliance Specialist</p>
                  <p className="navbar__profile-status">
                    <span className="navbar__status-dot" aria-hidden />
                    Active Session
                  </p>
                </div>
                <button
                  type="button"
                  className="navbar__logout"
                  onClick={() => setProfileOpen(false)}
                >
                  Logout
                </button>
              </div>
            )}
          </div>

          <button
            type="button"
            className={`navbar__hamburger ${menuOpen ? 'navbar__hamburger--open' : ''}`}
            aria-expanded={menuOpen}
            aria-controls="primary-nav"
            aria-label={menuOpen ? 'Close menu' : 'Open menu'}
            onClick={() => setMenuOpen((v) => !v)}
          >
            <span />
            <span />
            <span />
          </button>
        </div>
      </div>
    </header>
  )
}
