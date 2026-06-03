import jpype

jvm_path = r"C:\Program Files\Java\jdk-21.0.10\bin\server\jvm.dll"
sample_jar = r"C:\Users\mnsbartolata\Documents\NetBeansProjects\Sample\target\Sample-1.0-SNAPSHOT.jar"
mysql_jar = r"C:\Users\mnsbartolata\.m2\repository\mysql\mysql-connector-java\5.1.49\mysql-connector-java-5.1.49.jar"

jpype.startJVM(
    jvm_path,
    classpath=[
        sample_jar,
        mysql_jar
    ]
)

DBConnect = jpype.JClass("com.mycompany.sample.DBConnect")
Sample = jpype.JClass("com.mycompany.sample.Sample")

connected = DBConnect.connect()

print("Connected status", connected)

obj = Sample()
print(obj.getName())
obj.SaveRecord(
    6969,
    "Juan Dela Cruz",
    "Davao City",
    "BSIT",
    "Male",
    "1st Year"
)
