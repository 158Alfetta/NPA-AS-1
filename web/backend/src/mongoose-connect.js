  
import mongoose from 'mongoose'
const options = {
  dbName: process.env.DB_NAME,
  user: process.env.DB_USER,
  pass: process.env.DB_PASS,
  promiseLibrary: Promise,
  useNewUrlParser: true,
  useUnifiedTopology: true,
  useCreateIndex: true,
  useFindAndModify: false,
}
mongoose
  .connect(process.env.MONGO_DB_URL, options)
  .then(() => console.log('MongoDB Connected...'))
  .catch((err) => console.log(err))