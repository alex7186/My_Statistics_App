from classes import StatAnalysis_1_arr, StatAnalysis_2_arr
from graph import StatAnalysis_1_arr_make_boxplot, StatAnalysis_1_arr_make_hist, StatAnalysis_1_true_plot, StatAnalysis_2_arr_make_boxplot
from side_functions import _decode_buff_to_bytes

from datetime import datetime
from json import dumps, loads
from json.decoder import JSONDecodeError
from io import BytesIO
from aiohttp import web

print(str(datetime.now())[:-7], ' - server started')

def arr_1_server_answer(
    arr, sr_methodics=-10, 
    true_value=-10, 
    make_text=0, 
    param_make_hist=0, 
    param_make_boxplot=0):

    result = [
        {'type':'text',  'show_index':0, 'content': ""},
        {'type':'image', 'show_index':1, 'content': ""},
        {'type':'text',  'show_index':2, 'content': ""},
        {'type':'image', 'show_index':3, 'content': ""},
        {'type':'text',  'show_index':4, 'content': ""},
        {'type':'image', 'show_index':5, 'content': ""},
    ]

    if make_text or (true_value > -1):
        analysis = StatAnalysis_1_arr(arr, sr_methodics=sr_methodics, true_value=true_value)
        text_arr = analysis.res_text[0]
        result[0]['content'] = text_arr[0]

    if param_make_hist:
       # result[1]['content'] = _decode_buff_to_bytes(StatAnalysis_1_arr_make_hist(sorted(analysis.arr)))
       result[1]['content'] = _decode_buff_to_bytes(StatAnalysis_1_arr_make_hist(sorted(arr)))
    
    if make_text:
        result[2]['content'] = text_arr[1]
    
    if param_make_boxplot:
       # result[3]['content'] = _decode_buff_to_bytes(StatAnalysis_1_arr_make_boxplot(sorted(analysis.arr)))
       result[3]['content'] = _decode_buff_to_bytes(StatAnalysis_1_arr_make_boxplot(sorted(arr)))
    
    if make_text:
        result[4]['content'] = text_arr[2]

    if true_value > -1:
       # result[5]['content'] = _decode_buff_to_bytes(StatAnalysis_1_true_plot(analysis.arr, true_value))
       result[5]['content'] = _decode_buff_to_bytes(StatAnalysis_1_true_plot(arr, true_value))

    return result

def arr_2_server_answer(
    arr1, 
    arr2, 
    make_text=0, 
    param_make_2_boxplots=0):
    result = [
        {'type':'text',  'show_index':0, 'content': ""},
        {'type':'image', 'show_index':1, 'content': ""},
        {'type':'text',  'show_index':2, 'content': ""},
        # {'type':'image', 'show_index':2, 'content': ""},
    ]

    if make_text:
        text_arr = StatAnalysis_2_arr(arr1, arr2).res_text[0]
        result[0]['content'] = text_arr[0]
    if param_make_2_boxplots:
        result[1]['content'] = _decode_buff_to_bytes(StatAnalysis_2_arr_make_boxplot(sorted(arr1), sorted(arr2)))
    if make_text:
        result[2]['content'] = text_arr[1]

    return result


app = web.Application()

async def server(request):

    print(str(datetime.now())[:-7], ' - new request')

    # request_str = await request.read()
    # print(request_str)
    # try:
    #     data = loads(request_str)        
    # except JSONDecodeError:
    #     print(str(datetime.now())[:-7], ' - input JSONDecodeError')
    #     return web.Response(text='input JSONDecodeError')

    server_return = arr_1_server_answer(
        [42.0, 42.5, 41.9, 41.5, 41.8],
        -100,
        -100,
        1,
        0,
        0,)

    # if data['req_type'] == '1_arr':

    #     server_return = arr_1_server_answer(
    #         data['arr_data'], 
    #         data['sr_met'], 
    #         data['true_value'], 
    #         data['make_text'], 
    #         data['make_hist'], 
    #         data['make_boxplot']
    #         )

    # elif data['req_type'] == '2_arr':
    #     server_return = arr_2_server_answer(
    #         data['arr1'], data['arr2'], data['make_text'], data['make_boxplot']
    #         )

    return web.Response(text=dumps(server_return))
    
app.add_routes([web.post('/', server, ), web.get('/', server)])
web.run_app(app, port=5001)
