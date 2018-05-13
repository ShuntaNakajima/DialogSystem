post_install do |installer|
find_and_replace("google")

#Show BUILDFIXES
puts "\n--------BUILDFIXES--------\n"
puts "Fixing Protocol Buffer toolchain issues"
find_and_replace("google")
puts "----------------------------\n\n"

end

def find_and_replace(dir)
  Dir[dir + '*.*'].each do |name|
        text = File.read(name)

        replace = text.gsub("\"google/cloud/speech/v1beta1/CloudSpeech.pbobjc.h\"", "<googleapis/CloudSpeech.pbobjc.h>")
        replace = replace.gsub("\"google/api/Annotations.pbobjc.h\"", "<googleapis/Annotations.pbobjc.h>")
        replace = replace.gsub("\"google/longrunning/Operations.pbobjc.h\"", "<googleapis/Operations.pbobjc.h>")
        replace = replace.gsub("\"google/rpc/Status.pbobjc.h\"", "<googleapis/Status.pbobjc.h>")

        if text != replace
            puts "Fixing " + name
            File.open(name, "w") { |file| file.puts replace }
            STDOUT.flush
        end
  end
  Dir[dir + '*/'].each(&method(:find_and_replace))
end```
