import { useId } from 'react'

/** DNA helix + shield + document check — minimal enterprise mark */
export default function RegulatoryLogo({ className = '' }) {
  const gid = `ra-logo-${useId().replace(/:/g, '')}`

  return (
    <svg
      className={className}
      viewBox="0 0 40 40"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden
      width="40"
      height="40"
    >
      <defs>
        <linearGradient id={`${gid}-s`} x1="12" y1="4" x2="34" y2="34" gradientUnits="userSpaceOnUse">
          <stop stopColor="var(--logo-a)" />
          <stop offset="1" stopColor="var(--logo-b)" />
        </linearGradient>
        <linearGradient id={`${gid}-d`} x1="2" y1="10" x2="10" y2="30" gradientUnits="userSpaceOnUse">
          <stop stopColor="var(--logo-c)" />
          <stop offset="1" stopColor="var(--logo-d)" />
        </linearGradient>
      </defs>

      {/* DNA helix (left) */}
      <path
        d="M3 9c1.8 1.5 3 3.8 3 6.2s-1.2 4.7-3 6.2M9 9c-1.8 1.5-3 3.8-3 6.2s1.2 4.7 3 6.2"
        stroke={`url(#${gid}-d)`}
        strokeWidth="1.6"
        strokeLinecap="round"
        fill="none"
      />
      <line x1="4.5" y1="13" x2="7.5" y2="13" stroke="var(--logo-rung)" strokeWidth="1" strokeLinecap="round" />
      <line x1="4" y1="16.5" x2="8" y2="16.5" stroke="var(--logo-rung)" strokeWidth="1" strokeLinecap="round" />
      <line x1="4.5" y1="20" x2="7.5" y2="20" stroke="var(--logo-rung)" strokeWidth="1" strokeLinecap="round" />

      {/* Shield */}
      <path
        d="M20 4.2L33.2 9.2c.5.2.8.7.8 1.2v10.2c0 6.2-4.5 11.4-13.2 14.8a1.2 1.2 0 01-1.6 0C10.5 32 6 26.8 6 20.6V10.4c0-.5.3-1 .8-1.2L20 4.2Z"
        stroke={`url(#${gid}-s)`}
        strokeWidth="1.35"
        fill="var(--logo-shield-fill)"
      />

      {/* Document */}
      <rect x="14.5" y="12" width="11" height="14" rx="1.2" fill="var(--logo-doc)" stroke="var(--logo-doc-stroke)" strokeWidth="0.9" />
      <path
        d="M17 17.5l2 2 4.5-4.5"
        stroke="var(--logo-check)"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <line x1="17" y1="22" x2="23" y2="22" stroke="var(--logo-lines)" strokeWidth="1" strokeLinecap="round" />
    </svg>
  )
}
