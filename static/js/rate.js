 function Rate_question(id, type)
        { 
            token = document.cookie.match(/csrftoken=([^;]*)/) && RegExp.$1
            $.ajax({
                url: '/rate/',
                data: {q_id: id, type: type, csrfmiddlewaretoken: token},
                type: 'POST',
                success: function (jsondata) {
                    $('#q_rating'+id).html(jsondata.likes);
                }
            });

        }

