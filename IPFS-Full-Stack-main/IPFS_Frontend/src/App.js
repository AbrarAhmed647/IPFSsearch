import { Routes, Route } from 'react-router-dom' 
import Layout from './components/Layout'
import Welcome from './features/Welcome'
import DashLayout from './components/DashLayout'
import FileList from './features/FileList'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Welcome />} />
        <Route path="dash" element={<DashLayout />}>
        <Route index element={<FileList />} />
        </Route>

      </Route>
    </Routes>
  );
}

export default App;