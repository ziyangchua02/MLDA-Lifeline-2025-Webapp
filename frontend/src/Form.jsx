const { useState } = React;

const FIELDS = [
  'LB','AC','FM','UC','ASTV','MSTV','ALTV','MLTV','DL','DS','DP','Width','Mode','Mean','Median','Variance','Tendency'
];

export default function Form({ onResult }){
  const initial = FIELDS.reduce((a,f)=> (a[f]='',a), {});
  const [form,setForm] = useState(initial);
  const [loading,setLoading] = useState(false);

  function handleChange(e){
    const {name,value} = e.target;
    setForm(prev=>({...prev,[name]:value}));
  }

  async function handleSubmit(e){
    e.preventDefault();
    setLoading(true);
    onResult(null);
    const payload = {};
    for(const k of FIELDS) payload[k]=parseFloat(form[k]);
    try{
      const res = await fetch('/predict',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
      const json = await res.json();
      if(res.ok && json.prediction) onResult({ok:true,text:json.prediction});
      else onResult({ok:false,text:json.error||JSON.stringify(json)});
    }catch(err){
      onResult({ok:false,text:err.message});
    }finally{setLoading(false)}
  }

  function fillSample(){
    const sample = {LB:2,AC:10,FM:0,UC:1,ASTV:0,MSTV:30,ALTV:0,MLTV:0,DL:0,DS:0,DP:0,Width:0,Mode:120,Mean:120,Median:120,Variance:0,Tendency:0};
    setForm(sample);
  }

  return (
    <form onSubmit={handleSubmit}>
      {FIELDS.map(f=> (
        <div key={f}>
          <label htmlFor={f}>{f}</label>
          <input id={f} name={f} type="number" step="any" required value={form[f]} onChange={handleChange} />
        </div>
      ))}

      <div>
        <button type="submit" disabled={loading}>{loading? 'Predicting...' : 'Predict'}</button>
        <button type="button" onClick={fillSample}>Fill sample</button>
      </div>
    </form>
  );
}
