	  program water_sdf
!
!   program to make sdf file for water constellation
!
	  character*4 atnam(100)
	  character*20 drugnm
      dimension c(100,3)
      dimension distat(100,100)
      dimension ifound(100)
      integer cin,cout,cpdb
      data cin/1/,cout/2/,cpdb/3/
!
!  open input and output files
!
      open (unit=cin,file='data.in',status='old')
      open (unit=cpdb,file='in_water.pdb',status='old')
      open (unit=cout,file='out_water.sdf',status='new')
! iopt = 0 original code; iopt = 1 make multiple sdfs
      read (cin,1500) iopt
1500  format (i2)
      read (cin,1510) drugnm
1510  format (a20)
!      drugnm = trim(drugnm)
1000  format (12x,a4,14x,3f8.3)                                                         
      n = 0                                                   
10    n = n + 1
      read (cpdb,1000,end=20) atnam(n), c(n,1), c(n,2), c(n,3)
      goto 10
20    natoms = n - 1
      do 30, n1 = 1,natoms
        do 40, n2 = 1,natoms
          call distij (c(n1,1),c(n2,1),c(n1,2),c(n2,2),c(n1,3),c(n2,3),d)
          distat(n1,n2) = d
40      continue
30    continue
!      do 50, n1 = 1,natoms
!        write (cout,2000) n1, (distat(n1,n2),n2=1,natoms)
!50    continue
!2000  format (i4,20f6.1)
!
      nwat = 0
15    nwat = nwat + 1   
      if (iopt.eq.0) write (cout,2010) natoms, natoms-1
2010  format ("water constellation",/,"  ViewerPro         3D                             0",/,/,2i3,"  0  0  0  0  0  0  0  0999 V2000")   
      if (iopt.eq.1) write (cout,2011) nwat, drugnm, natoms, natoms-1
2011  format ("water constellation",i3,1x,a20,/,"  ViewerPro         3D                             0",/,/,2i3,"  0  0  0  0  0  0  0  0999 V2000")
      do 60, n = 1,natoms
        write (cout,2020) c(n,1), c(n,2), c(n,3), atnam(n)(2:2), n
60    continue
2020  format (3f10.4,1x,a1,"   0  0  0  0  0  0  0  0  0",i3)
!
      if (iopt.eq.0) then
        dhigh = 0.0
        do 70, n1 = 1,natoms
          dlown1 = 10000.0   
          do 80, n2 = 1,natoms
            if (n1.eq.n2) goto 80  
            if (distat(n1,n2).lt.dlown1) then
              dlown1 = distat(n1,n2)
              n2cnn1 = n2
            end if
80        continue
          if (dlown1.gt.dhigh) then
            dhigh = dlown1
            iatfir = n1
            iatsec = n2cnn1
          end if
70      continue
      else if (iopt.eq.1) then
        iatfir = nwat
        dlown1 = 10000.0   
        do 85, n2 = 1,natoms
          if (iatfir.eq.n2) goto 85  
          if (distat(iatfir,n2).lt.dlown1) then
            dlown1 = distat(iatfir,n2)
            iatsec = n2
          end if
85      continue
      end if
!      write (cout,3434) iatfir, iatsec, dhigh
!3434  format (2i4,f7.2)
!
      do 90, n=1,natoms
        ifound(n) = 0
90    continue 
      do 100, k=1,natoms-1
        if (k.eq.1) then
          ifound(iatfir) = 1
          write (cout,2100) iatfir, iatsec
2100      format (2i3,"  1  0  0  0")
          iatcur = iatsec
        else
          dlow = 10000.0
          do 110, n=1,natoms
            if (ifound(n).eq.0.and.n.ne.iatcur) then
              if (distat(iatcur,n).lt.dlow) then
                iatnxt = n
                dlow = distat(iatcur,n)
              end if
            end if
110       continue
          if (dlow.lt.4.0) then
            write (cout,2100) iatcur, iatnxt
            ifound(iatcur) = 1
            iatcur = iatnxt
          else  
            ifound(iatcur) = 1
            dlow2 = 4.0
            do 120, n1=1,natoms
              if (ifound(n1).eq.1) then
                do 130, n2=1,natoms
                  if (ifound(n2).eq.0) then
                    if (distat(n1,n2).lt.dlow2) then
                      dlow2 = distat(n1,n2)
                      iatcur = n1
                      iatnxt = n2
                    end if
                  end if
130             continue
              end if
120         continue
            write (cout,2100) iatcur, iatnxt
            iatcur = iatnxt
          end if  
        end if
100   continue
      write (cout,2110)
2110  format ("M  END",/,"$$$$")
      if (iopt.eq.1.and.nwat.lt.natoms) goto 15
!
      stop
      end
!
      subroutine distij (x1,x2,y1,y2,z1,z2,d)
        d = sqrt( ((x1-x2)**2) + ((y1-y2)**2) + ((z1-z2)**2) )          
      return
      end   