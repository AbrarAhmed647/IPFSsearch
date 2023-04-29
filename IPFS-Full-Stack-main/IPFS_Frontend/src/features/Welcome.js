import { Link } from 'react-router-dom';
import '../styles.css';

const Welcome = () => {
  const date = new Date();
  const today = new Intl.DateTimeFormat('en-US', {
    dateStyle: 'full',
    timeStyle: 'long',
  }).format(date);

  return (
    <section className="flex flex-col items-center justify-center h-screen">
      <p>{today}</p>
      <h1 className="text-3xl font-bold mb-8">IPFS Keyword Search</h1>
      <p className="mb-8">This app requires permission and authorization to access your IPFS information, which includes granting access to your IPFS node.</p>
      <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
        <Link to="/dash">Confirm</Link>
      </button>
    </section>
  );
};

export default Welcome;
