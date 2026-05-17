# Prototyping: AI Courses Catalog Platform

## Prompt Used in Anthropic Claude (Artifacts Feature)

> I am attaching a complete set of user stories and feature decomposition for an **AI Courses Catalog** web platform. Based on these materials, generate a fully interactive prototype as a single React component using the Claude Artifacts feature.
>
> Requirements:
> 1. Implement the catalog page with a responsive course card grid (3–4 columns desktop, 1 column mobile).
> 2. Each course card must display: thumbnail (gradient placeholder), title, category badge, difficulty badge (color-coded), duration, instructor, star rating, learner count, enrollment CTA button, and a bookmark icon.
> 3. Implement a working keyword search bar with live filtering.
> 4. Implement working filter dropdowns for Category, Difficulty, and Duration.
> 5. Implement a working Sort By control (Most Popular, Highest Rated, Newest, A–Z).
> 6. Show active filter chips below the filter bar with individual remove buttons and a "Clear all" button.
> 7. Show a results count label (e.g., "Showing 8 of 24 courses").
> 8. Enrollment CTA buttons must be state-aware: "Enroll Now" → "Start Course" → "Continue" → "Review Course" on click cycling.
> 9. Bookmark icon must toggle on/off with visual state change.
> 10. Show a per-card progress bar for in-progress courses.
> 11. Role indicator badge in the header (Learner / Instructor / Admin) that cycles on click.
> 12. User avatar dropdown menu in the top-right corner with: My Profile, My Courses, Settings, Logout links.
> 13. Use Tailwind CSS utility classes for all styling — no external CSS files.
> 14. Use React hooks (useState, useMemo) — no external state management.
> 15. The component must be completely self-contained with all mock data inline.
> 16. Enhance using Lucide React icons where appropriate (Search, Bookmark, Star, User, ChevronDown, X, Filter, etc.).

---

## Outcome of Prompt Execution

### Generated Interactive React Prototype

```jsx
import { useState, useMemo } from "react";
import {
  Search, Bookmark, BookmarkCheck, Star, User, ChevronDown,
  X, Clock, Users, BookOpen, LogOut, Settings, Library,
  PlusCircle, Filter, GraduationCap, BarChart2
} from "lucide-react";

// ─── Mock Data ───────────────────────────────────────────────────────────────
const COURSES = [
  {
    id: 1, title: "Introduction to Generative AI", category: "Generative AI",
    level: "Beginner", duration: 120, instructor: "Dr. Sarah Chen",
    rating: 4.8, reviews: 1240, learners: 8900, updated: "2025-03-01",
    color: "from-violet-500 to-purple-700",
  },
  {
    id: 2, title: "Prompt Engineering for Developers", category: "Generative AI",
    level: "Intermediate", duration: 210, instructor: "Mark Rivera",
    rating: 4.6, reviews: 875, learners: 5400, updated: "2025-02-15",
    color: "from-blue-500 to-indigo-700",
  },
  {
    id: 3, title: "Machine Learning Fundamentals", category: "Machine Learning",
    level: "Beginner", duration: 360, instructor: "Prof. Alan Turing Jr.",
    rating: 4.9, reviews: 2100, learners: 14200, updated: "2025-01-20",
    color: "from-emerald-500 to-teal-700",
  },
  {
    id: 4, title: "Deep Learning with PyTorch", category: "Machine Learning",
    level: "Advanced", duration: 540, instructor: "Dr. Lisa Park",
    rating: 4.7, reviews: 630, learners: 3200, updated: "2025-03-10",
    color: "from-rose-500 to-pink-700",
  },
  {
    id: 5, title: "Natural Language Processing Essentials", category: "NLP",
    level: "Intermediate", duration: 300, instructor: "James Okafor",
    rating: 4.5, reviews: 410, learners: 2800, updated: "2024-12-05",
    color: "from-amber-500 to-orange-700",
  },
  {
    id: 6, title: "Computer Vision with OpenCV", category: "Computer Vision",
    level: "Intermediate", duration: 420, instructor: "Dr. Emma Schulz",
    rating: 4.4, reviews: 320, learners: 1900, updated: "2025-01-10",
    color: "from-cyan-500 to-sky-700",
  },
  {
    id: 7, title: "AI Ethics and Responsible AI", category: "AI Ethics",
    level: "Beginner", duration: 90, instructor: "Dr. Priya Nair",
    rating: 4.7, reviews: 580, learners: 4100, updated: "2025-03-05",
    color: "from-fuchsia-500 to-purple-700",
  },
  {
    id: 8, title: "Reinforcement Learning Mastery", category: "Machine Learning",
    level: "Advanced", duration: 600, instructor: "Prof. Kai Zhang",
    rating: 4.6, reviews: 220, learners: 1100, updated: "2024-11-20",
    color: "from-lime-500 to-green-700",
  },
  {
    id: 9, title: "LLM Fine-tuning and RAG Systems", category: "Generative AI",
    level: "Advanced", duration: 480, instructor: "Dr. Sarah Chen",
    rating: 4.9, reviews: 315, learners: 2600, updated: "2025-03-12",
    color: "from-sky-500 to-blue-700",
  },
  {
    id: 10, title: "Data Science for AI Practitioners", category: "Data Science",
    level: "Beginner", duration: 270, instructor: "Maria Santos",
    rating: 4.3, reviews: 760, learners: 6200, updated: "2024-10-15",
    color: "from-teal-500 to-emerald-700",
  },
  {
    id: 11, title: "Transformer Architectures Explained", category: "NLP",
    level: "Advanced", duration: 330, instructor: "James Okafor",
    rating: 4.8, reviews: 290, learners: 1700, updated: "2025-02-28",
    color: "from-orange-500 to-red-700",
  },
  {
    id: 12, title: "MLOps: Deploying AI at Scale", category: "Machine Learning",
    level: "Intermediate", duration: 390, instructor: "Dr. Lisa Park",
    rating: 4.5, reviews: 445, learners: 3500, updated: "2025-01-30",
    color: "from-indigo-500 to-violet-700",
  },
];

const CATEGORIES = ["All", "Generative AI", "Machine Learning", "NLP", "Computer Vision", "Data Science", "AI Ethics"];
const LEVELS = ["All", "Beginner", "Intermediate", "Advanced"];
const DURATIONS = ["All", "Under 2h", "2–5h", "5–10h", "10h+"];
const SORTS = ["Most Popular", "Highest Rated", "Newest", "A–Z"];
const ROLES = ["Learner", "Instructor", "Admin"];

const LEVEL_COLORS = {
  Beginner: "bg-emerald-100 text-emerald-700",
  Intermediate: "bg-amber-100 text-amber-700",
  Advanced: "bg-rose-100 text-rose-700",
};

const ENROLL_STATES = ["Enroll Now", "Start Course", "Continue", "Review Course"];
const ENROLL_COLORS = [
  "bg-violet-600 hover:bg-violet-700",
  "bg-blue-600 hover:bg-blue-700",
  "bg-emerald-600 hover:bg-emerald-700",
  "bg-slate-600 hover:bg-slate-700",
];

function formatDuration(minutes) {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return m > 0 ? `${h}h ${m}min` : `${h}h`;
}

function StarRating({ rating }) {
  return (
    <div className="flex items-center gap-1">
      {[1, 2, 3, 4, 5].map((s) => (
        <Star
          key={s}
          size={12}
          className={s <= Math.round(rating) ? "text-amber-400 fill-amber-400" : "text-slate-300 fill-slate-300"}
        />
      ))}
      <span className="text-xs font-semibold text-slate-700 ml-0.5">{rating.toFixed(1)}</span>
    </div>
  );
}

function CourseCard({ course, enrollState, onEnroll, bookmarked, onBookmark }) {
  const progress = enrollState === 2 ? 65 : enrollState === 3 ? 100 : 0;
  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden flex flex-col hover:shadow-md transition-shadow duration-200 group">
      {/* Thumbnail */}
      <div className={`bg-gradient-to-br ${course.color} h-36 relative flex items-center justify-center`}>
        <GraduationCap size={48} className="text-white/70" />
        <button
          onClick={() => onBookmark(course.id)}
          className="absolute top-3 right-3 bg-white/20 hover:bg-white/40 backdrop-blur-sm rounded-full p-1.5 transition-colors"
          title={bookmarked ? "Remove from Wishlist" : "Add to Wishlist"}
        >
          {bookmarked
            ? <BookmarkCheck size={16} className="text-white fill-white" />
            : <Bookmark size={16} className="text-white" />}
        </button>
        {enrollState === 3 && (
          <div className="absolute top-3 left-3 bg-emerald-500 text-white text-xs font-bold px-2 py-0.5 rounded-full">
            ✓ Completed
          </div>
        )}
      </div>

      {/* Body */}
      <div className="p-4 flex flex-col flex-1 gap-2">
        {/* Badges */}
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs bg-violet-100 text-violet-700 font-medium px-2 py-0.5 rounded-full">
            {course.category}
          </span>
          <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${LEVEL_COLORS[course.level]}`}>
            {course.level}
          </span>
        </div>

        {/* Title */}
        <h3 className="font-semibold text-slate-800 text-sm leading-snug line-clamp-2 group-hover:text-violet-700 transition-colors">
          {course.title}
        </h3>

        {/* Instructor */}
        <p className="text-xs text-slate-500">{course.instructor}</p>

        {/* Rating */}
        <StarRating rating={course.rating} />

        {/* Meta row */}
        <div className="flex items-center gap-3 text-xs text-slate-500 mt-auto">
          <span className="flex items-center gap-1">
            <Clock size={11} /> {formatDuration(course.duration)}
          </span>
          <span className="flex items-center gap-1">
            <Users size={11} /> {course.learners.toLocaleString()}
          </span>
        </div>

        {/* Progress bar */}
        {(enrollState === 2 || enrollState === 3) && (
          <div className="mt-1">
            <div className="flex justify-between text-xs text-slate-500 mb-1">
              <span>Progress</span>
              <span>{progress}%</span>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-1.5">
              <div
                className="bg-violet-500 h-1.5 rounded-full transition-all"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        )}

        {/* CTA */}
        <button
          onClick={() => onEnroll(course.id)}
          className={`mt-2 w-full text-white text-sm font-medium py-2 rounded-xl transition-colors ${ENROLL_COLORS[enrollState]}`}
        >
          {ENROLL_STATES[enrollState]}
        </button>
      </div>
    </div>
  );
}

export default function App() {
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All");
  const [level, setLevel] = useState("All");
  const [duration, setDuration] = useState("All");
  const [sort, setSort] = useState("Most Popular");
  const [enrollStates, setEnrollStates] = useState({});
  const [bookmarks, setBookmarks] = useState({});
  const [roleIdx, setRoleIdx] = useState(0);
  const [profileOpen, setProfileOpen] = useState(false);

  const role = ROLES[roleIdx];

  // Filter chips
  const chips = [
    category !== "All" && { key: "category", label: `Category: ${category}`, clear: () => setCategory("All") },
    level !== "All" && { key: "level", label: `Level: ${level}`, clear: () => setLevel("All") },
    duration !== "All" && { key: "duration", label: `Duration: ${duration}`, clear: () => setDuration("All") },
  ].filter(Boolean);

  const clearAll = () => { setCategory("All"); setLevel("All"); setDuration("All"); setSearch(""); };

  // Filtering & sorting
  const filtered = useMemo(() => {
    let list = COURSES.filter((c) => {
      const matchSearch = c.title.toLowerCase().includes(search.toLowerCase()) ||
        c.category.toLowerCase().includes(search.toLowerCase()) ||
        c.instructor.toLowerCase().includes(search.toLowerCase());
      const matchCat = category === "All" || c.category === category;
      const matchLevel = level === "All" || c.level === level;
      const matchDur = duration === "All" || (
        duration === "Under 2h" ? c.duration < 120 :
        duration === "2–5h" ? c.duration >= 120 && c.duration <= 300 :
        duration === "5–10h" ? c.duration > 300 && c.duration <= 600 :
        c.duration > 600
      );
      return matchSearch && matchCat && matchLevel && matchDur;
    });

    list = [...list].sort((a, b) =>
      sort === "Most Popular" ? b.learners - a.learners :
      sort === "Highest Rated" ? b.rating - a.rating :
      sort === "Newest" ? new Date(b.updated) - new Date(a.updated) :
      a.title.localeCompare(b.title)
    );
    return list;
  }, [search, category, level, duration, sort]);

  const handleEnroll = (id) =>
    setEnrollStates((s) => ({ ...s, [id]: ((s[id] ?? 0) + 1) % 4 }));

  const handleBookmark = (id) =>
    setBookmarks((b) => ({ ...b, [id]: !b[id] }));

  return (
    <div className="min-h-screen bg-slate-50 font-sans">

      {/* ── Header ─────────────────────────────────────────────────────── */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center gap-4">
          {/* Logo */}
          <div className="flex items-center gap-2 shrink-0">
            <div className="bg-gradient-to-br from-violet-600 to-indigo-600 rounded-xl p-1.5">
              <BookOpen size={18} className="text-white" />
            </div>
            <span className="font-bold text-slate-800 text-lg hidden sm:block">AI Academy</span>
          </div>

          {/* Search */}
          <div className="flex-1 relative">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search courses, topics, instructors…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-4 py-2 bg-slate-100 rounded-xl text-sm border border-transparent focus:border-violet-400 focus:outline-none focus:bg-white transition-colors"
            />
            {search && (
              <button onClick={() => setSearch("")} className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
                <X size={14} />
              </button>
            )}
          </div>

          {/* Instructor/Admin CTA */}
          {(role === "Instructor" || role === "Admin") && (
            <button className="hidden md:flex items-center gap-1.5 bg-violet-600 hover:bg-violet-700 text-white text-sm font-medium px-3 py-2 rounded-xl transition-colors shrink-0">
              <PlusCircle size={15} /> New Course
            </button>
          )}

          {/* Role badge + Avatar */}
          <div className="relative shrink-0">
            <button
              onClick={() => { setProfileOpen((o) => !o); }}
              className="flex items-center gap-2 hover:bg-slate-100 rounded-xl px-2 py-1.5 transition-colors"
            >
              <div className="bg-gradient-to-br from-violet-500 to-indigo-600 rounded-full w-8 h-8 flex items-center justify-center text-white text-xs font-bold">
                JD
              </div>
              <div className="hidden sm:flex flex-col items-start leading-tight">
                <span className="text-xs font-semibold text-slate-700">Jane Doe</span>
                <button
                  onClick={(e) => { e.stopPropagation(); setRoleIdx((i) => (i + 1) % 3); }}
                  className={`text-[10px] font-bold px-1.5 py-0.5 rounded-full cursor-pointer ${
                    role === "Admin" ? "bg-rose-100 text-rose-700" :
                    role === "Instructor" ? "bg-amber-100 text-amber-700" :
                    "bg-violet-100 text-violet-700"
                  }`}
                  title="Click to switch role (demo)"
                >
                  {role}
                </button>
              </div>
              <ChevronDown size={14} className="text-slate-400 hidden sm:block" />
            </button>

            {/* Dropdown */}
            {profileOpen && (
              <div className="absolute right-0 top-12 bg-white border border-slate-200 rounded-2xl shadow-xl w-48 py-1.5 z-50">
                <div className="px-4 py-2 border-b border-slate-100">
                  <p className="text-xs font-semibold text-slate-700">Jane Doe</p>
                  <p className="text-xs text-slate-400">jane@example.com</p>
                </div>
                {[
                  { icon: User, label: "My Profile" },
                  { icon: Library, label: "My Courses" },
                  { icon: Settings, label: "Settings" },
                  ...(role === "Admin" ? [{ icon: BarChart2, label: "Admin Panel" }] : []),
                ].map(({ icon: Icon, label }) => (
                  <button
                    key={label}
                    className="w-full flex items-center gap-2.5 px-4 py-2 text-sm text-slate-600 hover:bg-slate-50 transition-colors"
                    onClick={() => setProfileOpen(false)}
                  >
                    <Icon size={14} className="text-slate-400" /> {label}
                  </button>
                ))}
                <div className="border-t border-slate-100 mt-1">
                  <button
                    className="w-full flex items-center gap-2.5 px-4 py-2 text-sm text-rose-500 hover:bg-rose-50 transition-colors"
                    onClick={() => setProfileOpen(false)}
                  >
                    <LogOut size={14} /> Logout
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* ── Filters bar ─────────────────────────────────────────────────── */}
      <div className="bg-white border-b border-slate-100 sticky top-[61px] z-20">
        <div className="max-w-7xl mx-auto px-4 py-2.5 flex flex-wrap items-center gap-2">
          <Filter size={14} className="text-slate-400 shrink-0" />

          {/* Category */}
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="text-sm border border-slate-200 rounded-lg px-2.5 py-1.5 bg-white text-slate-700 focus:outline-none focus:border-violet-400 cursor-pointer"
          >
            {CATEGORIES.map((c) => <option key={c}>{c}</option>)}
          </select>

          {/* Level */}
          <select
            value={level}
            onChange={(e) => setLevel(e.target.value)}
            className="text-sm border border-slate-200 rounded-lg px-2.5 py-1.5 bg-white text-slate-700 focus:outline-none focus:border-violet-400 cursor-pointer"
          >
            {LEVELS.map((l) => <option key={l}>{l}</option>)}
          </select>

          {/* Duration */}
          <select
            value={duration}
            onChange={(e) => setDuration(e.target.value)}
            className="text-sm border border-slate-200 rounded-lg px-2.5 py-1.5 bg-white text-slate-700 focus:outline-none focus:border-violet-400 cursor-pointer"
          >
            {DURATIONS.map((d) => <option key={d}>{d}</option>)}
          </select>

          <div className="ml-auto flex items-center gap-2">
            <span className="text-xs text-slate-400 hidden sm:block">Sort:</span>
            <select
              value={sort}
              onChange={(e) => setSort(e.target.value)}
              className="text-sm border border-slate-200 rounded-lg px-2.5 py-1.5 bg-white text-slate-700 focus:outline-none focus:border-violet-400 cursor-pointer"
            >
              {SORTS.map((s) => <option key={s}>{s}</option>)}
            </select>
          </div>
        </div>

        {/* Active filter chips */}
        {chips.length > 0 && (
          <div className="max-w-7xl mx-auto px-4 pb-2.5 flex flex-wrap gap-2 items-center">
            {chips.map((chip) => (
              <span
                key={chip.key}
                className="flex items-center gap-1.5 bg-violet-50 text-violet-700 text-xs font-medium px-2.5 py-1 rounded-full border border-violet-200"
              >
                {chip.label}
                <button onClick={chip.clear} className="hover:text-violet-900">
                  <X size={11} />
                </button>
              </span>
            ))}
            <button
              onClick={clearAll}
              className="text-xs text-slate-400 hover:text-rose-500 underline underline-offset-2 transition-colors"
            >
              Clear all
            </button>
          </div>
        )}
      </div>

      {/* ── Main content ────────────────────────────────────────────────── */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        {/* Results count */}
        <div className="flex items-center justify-between mb-4">
          <p className="text-sm text-slate-500">
            Showing <span className="font-semibold text-slate-700">{filtered.length}</span> of{" "}
            <span className="font-semibold text-slate-700">{COURSES.length}</span> courses
          </p>
        </div>

        {/* Grid */}
        {filtered.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-24 text-slate-400">
            <Search size={40} className="mb-3 opacity-40" />
            <p className="text-lg font-semibold">No courses found</p>
            <p className="text-sm mt-1">Try adjusting your search or filters</p>
            <button
              onClick={clearAll}
              className="mt-4 bg-violet-600 text-white text-sm px-4 py-2 rounded-xl hover:bg-violet-700 transition-colors"
            >
              Reset filters
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
            {filtered.map((course) => (
              <CourseCard
                key={course.id}
                course={course}
                enrollState={enrollStates[course.id] ?? 0}
                onEnroll={handleEnroll}
                bookmarked={!!bookmarks[course.id]}
                onBookmark={handleBookmark}
              />
            ))}
          </div>
        )}

        {/* Pagination (UI only) */}
        {filtered.length > 0 && (
          <div className="flex justify-center items-center gap-2 mt-10">
            {["← Prev", "1", "2", "3", "Next →"].map((p) => (
              <button
                key={p}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                  p === "1"
                    ? "bg-violet-600 text-white"
                    : "bg-white border border-slate-200 text-slate-600 hover:bg-slate-50"
                }`}
              >
                {p}
              </button>
            ))}
          </div>
        )}
      </main>

      {/* Click-outside overlay for profile dropdown */}
      {profileOpen && (
        <div className="fixed inset-0 z-10" onClick={() => setProfileOpen(false)} />
      )}
    </div>
  );
}
```

---

## How to Run the Prototype

### Option A — Paste into StackBlitz / CodeSandbox

1. Go to [stackblitz.com/edit/react](https://stackblitz.com/edit/react) or [codesandbox.io](https://codesandbox.io).
2. Replace the default `App.jsx` with the code above.
3. Install Lucide icons: add `lucide-react` to `package.json` dependencies.
4. Add Tailwind CSS via CDN in `index.html`:
   ```html
   <script src="https://cdn.tailwindcss.com"></script>
   ```

### Option B — Local Vite + React setup

```bash
npm create vite@latest ai-academy -- --template react
cd ai-academy
npm install lucide-react
```

Add to `index.html` `<head>`:
```html
<script src="https://cdn.tailwindcss.com"></script>
```

Replace `src/App.jsx` with the component code above, then:
```bash
npm run dev
```

---

## Prototype Features Implemented

| User Story | Feature | Status |
|---|---|---|
| US-1-1 | Responsive course card grid (1/2/3/4 cols) | ✅ |
| US-1-2 | Full course card: title, badge, level, duration, instructor, rating, learners | ✅ |
| US-1-3 | Results count label ("Showing X of Y courses") | ✅ |
| US-2-1/2 | Live keyword search with clear button | ✅ |
| US-3-1/2/3 | Category, Difficulty, Duration filter dropdowns | ✅ |
| US-3-4 | Multi-filter AND logic | ✅ |
| US-3-5 | Active filter chips with individual remove + Clear all | ✅ |
| US-4-1/2/3/4 | Sort by Popular / Rated / Newest / A–Z | ✅ |
| US-5-1/3/4/5/6 | Enrollment CTA cycling: Enroll → Start → Continue → Review | ✅ |
| US-6-1 | Per-card progress bar for in-progress / completed courses | ✅ |
| US-7-1 | Bookmark toggle with filled/outline icon state | ✅ |
| US-8-1 | User avatar with dropdown profile menu | ✅ |
| US-8-5 | Logout menu item | ✅ |
| US-9-1/2/3 | Role badge cycling (Learner/Instructor/Admin) with conditional "New Course" button and "Admin Panel" menu item | ✅ |
| US-10-1 | Pagination controls (UI) | ✅ |
| US-10-2 | Responsive grid layout (Tailwind breakpoints) | ✅ |
| US-1-empty | Empty state with "Reset filters" CTA | ✅ |
