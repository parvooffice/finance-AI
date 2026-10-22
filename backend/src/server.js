import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import mongoose from 'mongoose';

const app=express();
app.use(cors({origin:true}));
app.use(express.json({limit:'1mb'}));
const journeySchema=new mongoose.Schema({key:{type:String,default:'default',unique:true},inputs:{type:mongoose.Schema.Types.Mixed,required:true},deductions:{type:[mongoose.Schema.Types.Mixed],default:[]},updatedAt:{type:Date,default:Date.now}},{minimize:false});
const Journey=mongoose.model('Journey',journeySchema);
let memoryJourney=null;
app.get('/api/health',(_req,res)=>res.json({status:'ok',service:'taxometer-api',database:mongoose.connection.readyState===1?'connected':'memory fallback'}));
app.get('/api/journey',async(_req,res)=>{try{const journey=mongoose.connection.readyState===1?await Journey.findOne({key:'default'}).lean():memoryJourney;res.json(journey||{});}catch(e){res.status(500).json({error:'Could not load your tax journey.'});}});
app.put('/api/journey',async(req,res)=>{const {inputs,deductions}=req.body||{};if(!inputs||!Array.isArray(deductions))return res.status(400).json({error:'Provide inputs and a deductions list.'});const payload={inputs,deductions,updatedAt:new Date()};try{if(mongoose.connection.readyState===1){const doc=await Journey.findOneAndUpdate({key:'default'},{$set:payload},{new:true,upsert:true});return res.json({saved:true,updatedAt:doc.updatedAt});}memoryJourney={key:'default',...payload};res.json({saved:true,storage:'memory',updatedAt:payload.updatedAt});}catch(e){res.status(500).json({error:'Could not save your tax journey.'});}});
app.post('/api/calculate',async(req,res)=>{try{const response=await fetch(`${process.env.FASTAPI_URL||'http://localhost:8000'}/calculate`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(req.body)});const data=await response.json();res.status(response.status).json(data);}catch{res.status(503).json({error:'Tax calculation service is unavailable.'});}});
const port=process.env.PORT||4000;
mongoose.connect(process.env.MONGODB_URI||'mongodb://127.0.0.1:27017/taxometer').then(()=>console.log('MongoDB connected')).catch(()=>console.warn('MongoDB unavailable; using in-memory journey storage.'));
app.listen(port,()=>console.log(`Taxometer API listening on http://localhost:${port}`));
