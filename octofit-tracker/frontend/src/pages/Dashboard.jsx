import { useEffect, useState } from 'react'

function Dashboard() {
  const [activities, setActivities] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function fetchActivities() {
      try {
        const response = await fetch('http://localhost:8000/api/activities/')
        if (!response.ok) {
          throw new Error('Failed to load activities')
        }
        const data = await response.json()
        setActivities(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchActivities()
  }, [])

  return (
    <div>
      <h1>OctoFit Activity Dashboard</h1>
      <p>Track fitness activities for Mergington High School.</p>

      {loading && <div className="alert alert-info">Loading activities...</div>}
      {error && <div className="alert alert-danger">{error}</div>}

      {!loading && !error && (
        <div>
          <div className="mb-4">
            <strong>Total activities:</strong> {activities.length}
          </div>

          <div className="table-responsive">
            <table className="table table-striped">
              <thead>
                <tr>
                  <th>User</th>
                  <th>Title</th>
                  <th>Description</th>
                  <th>Duration</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {activities.map((activity) => (
                  <tr key={activity.id}>
                    <td>{activity.user}</td>
                    <td>{activity.title}</td>
                    <td>{activity.description}</td>
                    <td>{activity.duration_minutes} min</td>
                    <td>{activity.date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}

export default Dashboard
