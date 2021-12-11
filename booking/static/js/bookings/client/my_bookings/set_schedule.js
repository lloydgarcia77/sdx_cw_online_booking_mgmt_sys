$(function() {
        
    //     $(function() {
    //   var today = new Date(),
    //     weekAgo = new Date(),
    //     $from = $("#StartDate"),
    //     $to = $("#EndDate");

    //   weekAgo.setDate(today.getDate() - 7);

    //   $from.datepicker({   
    //     maxDate: today,
    //     onSelect: function(dateText) {
    //       $to.datepicker("option", "minDate", dateText);
    //     }
    //   }).datepicker('setDate', weekAgo);

    //   $to.datepicker({
    //     maxDate: today,
    //     minDate: weekAgo,
    //     onSelect: function(dateText) {
    //       $from.datepicker("option", "maxDate", dateText);
    //     }
    //   }).datepicker('setDate', today);

    // });

    // Loads the JSON
    const schedule_data = JSON.parse(document.getElementById('schedule_data').textContent);
    const parsed_schedule_data = JSON.parse(schedule_data) 
    const TIME_SLOTS = [
        '08:00am - 10:00am',
        '10:00am - 12:00pm',
        '12:00pm - 02:00pm',
        '02:00pm - 04:00pm',
        '04:00pm - 06:00pm',
        '06:00am - 08:00pm',
    ]

    let today = new Date(), weekLater = new Date();
    weekLater.setDate(today.getDate() + 6); // Including today 
    // var array = ["2021-12-10","2021-12-11","2021-12-12"]
    
    // Date Picker Initial Setup
    $( "#datepicker" ).datepicker({
        // disable date 
        beforeShowDay: function(date){
            let string = $.datepicker.formatDate('yy-mm-dd', date);
            return [ parsed_schedule_data.fully_booked_dates.indexOf(string) == -1 ]
        },
        dateFormat: "yy-mm-dd" ,
        minDate: today,
        maxDate: weekLater,
        onSelect: function(dateText, inst) { 
            let date = $(this).val();   
            scheduleSelection();
            // var time = $('#time').val();
            // alert('on select triggered');
            // $("#start").val(date + time.toString(' HH:mm').toString());

        }
    });
 
    // Slot Navigation
    $("#select-slot").on("change", function(){
        scheduleSelection();
    });

    function scheduleSelection(){
        let text = $('#select-slot').find(":selected").text(); 
        let date = $( "#datepicker" ).datepicker("getDate");
        let string = $.datepicker.formatDate('yy-mm-dd', date);
        
    

        const [obj] = parsed_schedule_data.schedule_list.filter((e) => (
            e.date===string 
        ));
        

        function getSlot(){

            if (text==='Slot 1'){
                return obj.available_slots_slot1;
            }else if(text==='Slot 2'){
                return obj.available_slots_slot2;
            }else if (text==='Slot 3'){
                return obj.available_slots_slot3;
            }
  
        }

 
        const renderedTimeSchedule = TIME_SLOTS.map((e, i) => ( 
            `<div class="form-check">
                    <input class="form-check-input" type="radio" name="flexRadioDefault" value="${i+1}" id="time${i}" ${getSlot().includes(i+1) ? '' : 'disabled'}>
                    <label class="form-check-label" for="time${i}">
                        ${e}
                    </label>
            </div>`
        ));

        $("#time-schedule-container").html(renderedTimeSchedule);
    }

    // Default Initialization of Schedule selection
    scheduleSelection();


    // Submitting the action

    $(".btn-book").on("click", function(e){
        e.preventDefault();
        let slot = $('#select-slot').find(":selected").text(); 
        let date = $( "#datepicker" ).datepicker("getDate");
        let converted_date = $.datepicker.formatDate('yy-mm-dd', date);
        let time = $("input[name='flexRadioDefault']:checked").val();

        console.log(slot,converted_date,time)
        
        if(time===undefined){
            $("#modal-default").modal("show"); 
            $("#modal-default .modal-content").html(`
            <div class="modal-header">
                <h5 class="modal-title" id="modalDefaultLabel">Incomplete Schedule</h5>
                <button class="close" type="button" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">×</span>
                </button>
            </div>
            <div class="modal-body">
                Please select a schedule <b style="color:red;">TIME</b>.       
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" type="button" data-dismiss="modal">Close</button> 
            </div>
            `);
        }else{
            let url = $(this).attr("data-url");
             
            $.ajax({
                url: url,
                type: 'GET',
                dataType: 'json',
                beforeSend: () => { 
                    $("#modal-default").data("data", {date: converted_date, time: time, slot: slot}).modal("show"); 
                },
                success: (data) => {
                    $("#modal-default .modal-content").html(data.html_form);
                    $("#modal-default .modal-content .modal-body").append(`<p> 
                        Do you want to save your booking on <b>${converted_date}</b> at <b>${TIME_SLOTS[time]}</b> on <b>${slot}</b>?
                        </p>`);

                },
                complete: (data) => {

                },
                error: (data) => {

                }
            });
        }



        return false;
    })

    $("#modal-default").on("submit", ".booking-confirmation", function(e){
        e.preventDefault();
        let data = $("#modal-default").data('data'); 

        data = JSON.stringify(data);

        $.ajax({
            // https://docs.djangoproject.com/en/2.2/ref/csrf/
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: 'POST', // must be in POST
            url: $(this).attr('data-url'),
            data: {'data': data} , // json object to be transfer
            dataType: 'json',
            success: (data) => {
                if (data.form_is_valid) {
                    $("#modal-default").modal("hide"); 
                    // location.reload()
                    location.replace("/my-bookings/")
                }

            },
            complete: (data) => {

            },
            error: (data) => {

            }

        });

        return false;
    });

  });