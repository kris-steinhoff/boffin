import { useQuery, gql } from "@apollo/client";

const GET_STUDENTS = gql`
  query {
    students {
      id
      firstName
      lastName
    }
  }
`;

function DisplayStudents() {
  const { loading, error, data } = useQuery(GET_STUDENTS);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error : {error.message}</p>;

  return data.students.map(({ id, firstName, lastName }: { id: string, firstName: string, lastName: string }) => (

    <div key={id}>
      <h3>{firstName} {lastName}</h3>
    </div>
  ));

}
function App() {
  return (
    <div>
      <h2>My first Apollo app 🚀</h2>
      <br />
      <DisplayStudents />
    </div>
  )
}

export default App
