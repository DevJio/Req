docker exec -it flask-hello_flask_1 bash
docker exec -it flask-hello_flask_1 python train_model.py

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"id": [1,2,3,4,5,6],"text":["мама мыла раму","требуется мыть все рабочие плоскости оборудования составом с мылом, и не менее 18 раз","папа мыл раму","сестра мыла раму","конь мыл раму","лось мыл раму"]}' \
  http://localhost:5003/ds_post


Вы от нас будете ждать: 
json{ «id»: [id], «text»: [text]}
Где id – id абзацев
Text   – текстовки абзацев
 
В ответ будем получать:
json{ «id»: [id], «class»: [class]}
Где id – id абзацев
class  – классификация по абзацам

git remote add origin https://github.com/DevJio/web-service.git
git push -u origin master

chmod 400 "/Users/mikhail/keys/my_instance_web_service.pem"
ssh -i "/Users/mikhail/keys/my_instance_web_service.pem" ec2-user@ec2-35-180-254-61.eu-west-3.compute.amazonaws.com