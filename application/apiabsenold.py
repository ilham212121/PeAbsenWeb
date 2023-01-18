@app.route('/apiabsen',methods=['POST'])
def apiabsen():
    cur = mysql.connection.cursor()
    if 'image' not in request.files:
        cur.close()
        return jsonify({"msg":"tidak ada form image"})
    file = request.files['image']
    nip=request.form['nip']
    latitude=request.form['latitude']
    longitude= request.form['longitude']
    
    if file.filename == '':
        cur.close()
        return jsonify({"msg":"tidak ada file image yang dipilih"})
    if file and allowed_file(file.filename):
        print(file.filename)
        tanggal=""+str(thn)+"-"+str(bln)+"-"+str(hari)+""
        a=time.localtime()
        hr=a.tm_hour
        mn=a.tm_min
        thn=a.tm_year
        bln=a.tm_mon
        hari=a.tm_mday
        if hr>=12:
            if hr==12:
                hr=12
            else:
                hr = hr-12
            w='PM'
        else:
            if hr==0:
                hr=12
            w='AM'
        timeNow = str(hr)+':'+str(mn)+str(w)+''
        cur.execute("SELECT * from dataabsen where nip= %s and tanggal = %s ",(nip,tanggal))
        cek = cur.fetchall()
        if str(cek) == '()':
            cur.execute("SELECT jadwal.shift,shift.berangkat from jadwal INNER JOIN shift ON jadwal.shift = shift.nama where nip = %s,tanggal = %s",(nip,tanggal))
            shift = cur.fetchall()
            renamefile= secure_filename(str(nip)+str(tanggal)+str(timeNow)+".jpg")
            timeNow = datetime.strptime(timeNow, "%I:%M%p")
            timeEnd = datetime.strptime(shift[0][1], "%H:%M:%S")
            print(timeEnd)
            timeStart = datetime.strptime(timeEnd, "%H:%M"+-30+":%S")
            print(timeStart)
            status=isNowInTimePeriod(timeStart,timeEnd , timeNow)
            if shift[0][0]=="pagi":
                timeStart = '06:30AM'
                timeEnd = '07:10AM'
                timeEnd = datetime.strptime(timeEnd, "%I:%M%p")
                timeStart = datetime.strptime(timeStart, "%I:%M%p")
                status=isNowInTimePeriod(timeStart, timeEnd, timeNow)
                
            elif shift[0][0]=="siang":
                timeStart = '01:30PM'
                timeEnd = '02:10PM'
                timeEnd = datetime.strptime(timeEnd, "%I:%M%p")
                timeStart = datetime.strptime(timeStart, "%I:%M%p")
                status=isNowInTimePeriod(timeStart, timeEnd, timeNow)
                
            elif shift[0][0]=="middle":
                timeStart = '09:30AM'
                timeEnd = '10:10AM'
                timeEnd = datetime.strptime(timeEnd, "%I:%M%p")
                timeStart = datetime.strptime(timeStart, "%I:%M%p")
                status=isNowInTimePeriod(timeStart, timeEnd, timeNow)
    
            elif shift[0][0]=="malam":
                timeStart = '09:30PM'
                timeEnd = '10:00PM'
                timeEnd = datetime.strptime(timeEnd, "%I:%M%p")
                timeStart = datetime.strptime(timeStart, "%I:%M%p")
                status=isNowInTimePeriod(timeStart, timeEnd, timeNow)
                
            file.save(os.path.join(app.config['FOLDER_ABSEN'], renamefile))
            if status=='kamu absen terlalu cepat':
                cur.close()
                return jsonify({"msg":status})
            if status=="kamu terlambat":
                statusdb="telat"
                cur.execute("INSERT INTO dataabsen(nip,latitude,longitude,tanggal,waktu,foto,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nip,latitude,longitude,tanggal,timeNow,renamefile,statusdb))
                if mysql.connection.commit():
                    cur.close()
                return jsonify({"msg":status})
            if status=="kamu absen tepat waktu":
                statusdb="tepat waktu"
                cur.execute("INSERT INTO dataabsen(nip,latitude,longitude,tanggal,waktu,foto,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nip,latitude,longitude,tanggal,timeNow,renamefile,statusdb))
                if mysql.connection.commit():
                    cur.close()
                return jsonify({"msg":status,"waktu":timeNow,"tanggal":tanggal})
        else:
            return jsonify({"msg":"maaf kamu sudah absen"})
    else:
        cur.close()
        return "foto yang anda kirim invalid"
