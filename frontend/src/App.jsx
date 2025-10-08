import Form from './Form.jsx';

export default function App(){
  const [result,setResult] = React.useState(null);

  return (
    <div>
      <h1>CTG Predictor</h1>
      <p>Enter the 17 CTG features and click Predict.</p>
      <Form onResult={setResult} />

      {result && (
        <div>
          {result.ok ? <div>Prediction: {result.text}</div> : <div>Error: {result.text}</div>}
        </div>
      )}
    </div>
  );
}
