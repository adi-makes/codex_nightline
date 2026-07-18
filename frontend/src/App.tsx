import { useEffect, useState } from 'react'
import { BottomNav } from './components/BottomNav'
import { Icon } from './components/Icon'
import { AskPage, ExplorePage, HomePage, PlacePage, ProfilePage, TripsPage, type SavedTrip } from './pages'

export type Route = '/' | '/explore' | '/ask' | '/trips' | '/profile' | '/place'
const validRoutes: Route[] = ['/', '/explore', '/ask', '/trips', '/profile', '/place']
const getRoute = (): Route => validRoutes.includes(window.location.pathname as Route) ? window.location.pathname as Route : '/'
const savedTripsKey = 'ask-kochi-saved-trips'

function getSavedTrips(): SavedTrip[] {
  try {
    const stored = window.localStorage.getItem(savedTripsKey)
    const parsed: unknown = stored ? JSON.parse(stored) : []
    return Array.isArray(parsed) ? parsed as SavedTrip[] : []
  } catch {
    return []
  }
}

export function App() {
  const [route, setRoute] = useState<Route>(getRoute)
  const [darkMode, setDarkMode] = useState(() => window.localStorage.getItem('ask-kochi-dark-mode') === 'true')
  const [askDraft, setAskDraft] = useState('')
  const [askAutoPrompt, setAskAutoPrompt] = useState('')
  const [askFocusKey, setAskFocusKey] = useState(0)
  const [exploreFilter, setExploreFilter] = useState('')
  const [place, setPlace] = useState('Fort Kochi')
  const [savedTrips, setSavedTrips] = useState<SavedTrip[]>(getSavedTrips)
  const navigate = (next: Route) => { if (next !== route) { window.history.pushState({}, '', next); setRoute(next); window.scrollTo({ top: 0, behavior: 'smooth' }) } }
  const openAsk = (prompt = '', submitImmediately = false) => { setAskDraft(prompt); if (submitImmediately) setAskAutoPrompt(prompt); setAskFocusKey((key) => key + 1); navigate('/ask') }
  const openExplore = (filter = '') => { setExploreFilter(filter); navigate('/explore') }
  const openPlace = (name: string) => { setPlace(name); navigate('/place') }
  const saveTrip = (trip: SavedTrip) => setSavedTrips((all) => all.some((item) => item.id === trip.id) ? all : [trip, ...all])
  useEffect(() => { const onPopState = () => setRoute(getRoute()); window.addEventListener('popstate', onPopState); return () => window.removeEventListener('popstate', onPopState) }, [])
  useEffect(() => { document.title = route === '/' ? 'Ask Kochi — Your local city companion' : `${route.slice(1).replace(/^./, (letter) => letter.toUpperCase())} — Ask Kochi` }, [route])
  useEffect(() => { window.localStorage.setItem('ask-kochi-dark-mode', String(darkMode)); document.documentElement.style.colorScheme = darkMode ? 'dark' : 'light' }, [darkMode])
  useEffect(() => { window.localStorage.setItem(savedTripsKey, JSON.stringify(savedTrips)) }, [savedTrips])

  return <div className={`app-shell ${darkMode ? 'dark' : ''}`}>
    <header className="site-header"><button className="brand" onClick={() => navigate('/')} aria-label="Ask Kochi home">Ask <strong>Kochi</strong></button><nav className="desktop-nav" aria-label="Main navigation">{[['/', 'Home'], ['/explore', 'Explore'], ['/ask', 'Ask Kochi'], ['/trips', 'Trips'], ['/profile', 'Profile']].map(([path, label]) => <button className={route === path ? 'active' : ''} key={path} onClick={() => navigate(path as Route)}>{label}</button>)}</nav><div className="header-actions"><button className="header-icon" aria-label="Search Kochi" onClick={() => openExplore()}><Icon name="search" size={20} /></button><button className="profile-avatar" aria-label="Open profile" onClick={() => navigate('/profile')}>A</button></div></header>
    <main className="page-stack">
      <div hidden={route !== '/'}><HomePage openAsk={openAsk} openExplore={openExplore} openPlace={openPlace} /></div>
      <div hidden={route !== '/explore'}><ExplorePage initialFilter={exploreFilter} openPlace={openPlace} /></div>
      <div hidden={route !== '/ask'}><AskPage initialDraft={askDraft} autoPrompt={askAutoPrompt} focusKey={askFocusKey} onDraftConsumed={() => setAskDraft('')} onAutoPromptConsumed={() => setAskAutoPrompt('')} savedTrips={savedTrips} saveTrip={saveTrip} /></div>
      <div hidden={route !== '/trips'}><TripsPage openPlace={openPlace} savedTrips={savedTrips} /></div>
      <div hidden={route !== '/profile'}><ProfilePage darkMode={darkMode} setDarkMode={setDarkMode} /></div>
      <div hidden={route !== '/place'}><PlacePage name={place} goBack={() => window.history.back()} openAsk={openAsk} /></div>
    </main>
    {route !== '/place' && <BottomNav route={route} navigate={navigate} />}
  </div>
}
