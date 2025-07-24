import React, { useState, ChangeEvent, FormEvent } from 'react';
import './App.css';

const API_BASE = 'http://localhost:5000/api/pdf';

type Operation = 'merge' | 'split' | 'ocr';

function App() {
  const [operation, setOperation] = useState<Operation>('merge');
  const [files, setFiles] = useState<File[]>([]);
  const [splitRange, setSplitRange] = useState({ start: 1, end: 1 });
  const [progress, setProgress] = useState<number>(0);
  const [resultUrl, setResultUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files));
      setResultUrl(null);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files) {
      setFiles(Array.from(e.dataTransfer.files));
      setResultUrl(null);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };

  const handleOperationChange = (e: ChangeEvent<HTMLSelectElement>) => {
    setOperation(e.target.value as Operation);
    setResultUrl(null);
    setError(null);
  };

  const handleSplitRangeChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setSplitRange((prev) => ({ ...prev, [name]: Number(value) }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setProgress(0);
    setError(null);
    setResultUrl(null);
    try {
      const formData = new FormData();
      if (operation === 'merge') {
        if (files.length < 2) throw new Error('Select at least two PDF files to merge.');
        files.forEach((file) => formData.append('files', file));
      } else {
        if (files.length !== 1) throw new Error('Select a single PDF file.');
        formData.append('file', files[0]);
        if (operation === 'split') {
          formData.append('start', String(splitRange.start));
          formData.append('end', String(splitRange.end));
        }
      }
      const endpoint =
        operation === 'merge'
          ? `${API_BASE}/merge`
          : operation === 'split'
          ? `${API_BASE}/split`
          : `${API_BASE}/ocr`;
      const response = await fetch(endpoint, {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.error || 'Server error');
      }
      // Download blob
      const blob = await response.blob();
      setProgress(100);
      setResultUrl(URL.createObjectURL(blob));
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-8">
      <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-xl">
        <h1 className="text-2xl font-bold mb-4 text-center">Smart PDF Toolkit</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block font-semibold mb-1">Operation</label>
            <select
              className="w-full border rounded px-3 py-2"
              value={operation}
              onChange={handleOperationChange}
            >
              <option value="merge">Merge PDFs</option>
              <option value="split">Split PDF</option>
              <option value="ocr">OCR (Scanned PDF to Searchable)</option>
            </select>
          </div>
          <div
            className="mb-4 border-2 border-dashed rounded-lg p-6 text-center bg-gray-100 cursor-pointer"
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onClick={() => document.getElementById('file-input')?.click()}
          >
            <input
              id="file-input"
              type="file"
              accept="application/pdf"
              multiple={operation === 'merge'}
              className="hidden"
              onChange={handleFileChange}
            />
            <p className="text-gray-600">
              {files.length === 0
                ? 'Drag & drop PDF(s) here, or click to select.'
                : files.map((f) => `${f.name} (${(f.size / 1024 / 1024).toFixed(2)} MB)`).join(', ')}
            </p>
          </div>
          {operation === 'split' && (
            <div className="mb-4 flex gap-2">
              <div>
                <label className="block text-sm">Start Page</label>
                <input
                  type="number"
                  name="start"
                  min={1}
                  value={splitRange.start}
                  onChange={handleSplitRangeChange}
                  className="border rounded px-2 py-1 w-20"
                />
              </div>
              <div>
                <label className="block text-sm">End Page</label>
                <input
                  type="number"
                  name="end"
                  min={splitRange.start}
                  value={splitRange.end}
                  onChange={handleSplitRangeChange}
                  className="border rounded px-2 py-1 w-20"
                />
              </div>
            </div>
          )}
          {loading && (
            <div className="mb-2">
              <div className="w-full bg-gray-200 rounded-full h-2.5 mb-2">
                <div
                  className="bg-blue-500 h-2.5 rounded-full"
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
              <p className="text-sm text-gray-500">Processing...</p>
            </div>
          )}
          {error && <div className="text-red-600 mb-2">{error}</div>}
          <button
            type="submit"
            className="w-full bg-blue-600 text-white font-semibold py-2 rounded hover:bg-blue-700 transition"
            disabled={loading || files.length === 0}
          >
            {loading ? 'Processing...' : 'Start'}
          </button>
        </form>
        {resultUrl && (
          <div className="mt-4 text-center">
            <a
              href={resultUrl}
              download={
                operation === 'merge'
                  ? 'merged.pdf'
                  : operation === 'split'
                  ? 'split.pdf'
                  : 'ocr_output.pdf'
              }
              className="inline-block bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition"
            >
              Download Result
            </a>
          </div>
        )}
      </div>
      <footer className="mt-8 text-gray-400 text-xs">&copy; {new Date().getFullYear()} Smart PDF & Media Toolkit</footer>
    </div>
  );
}

export default App;
