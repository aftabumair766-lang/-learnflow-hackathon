export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-4xl font-bold mb-8">LearnFlow</h1>
      <p className="text-lg mb-4">AI-Powered Learning Platform</p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="border p-4 rounded">
          <h2 className="text-2xl font-bold">Students</h2>
          <p>Register and find tutors</p>
        </div>

        <div className="border p-4 rounded">
          <h2 className="text-2xl font-bold">Tutors</h2>
          <p>Offer your expertise</p>
        </div>

        <div className="border p-4 rounded">
          <h2 className="text-2xl font-bold">Matching</h2>
          <p>AI-powered connections</p>
        </div>
      </div>
    </main>
  )
}
