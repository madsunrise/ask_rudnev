function Correct_answer(q_id, a_id)
        { 
            token = document.cookie.match(/csrftoken=([^;]*)/) && RegExp.$1
            $.ajax({
                url: '/correct_answer/',
                data: {q_id: q_id, a_id: a_id, csrfmiddlewaretoken: token},
                type: 'POST',
                success: function (jsondata) {
                    $('#correct'+jsondata.old_id).prop("checked", false);
                }
            });

        }

