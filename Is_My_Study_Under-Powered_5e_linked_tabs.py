#!/usr/bin/env python
# coding: utf-8

# https://nbviewer.jupyter.org/github/bokeh/bokeh-notebooks/blob/master/quickstart/quickstart.ipynb

# In[48]:


import bokeh.plotting
import bokeh.layouts
import bokeh.io
import bokeh.models
import numpy as np
import pandas as pd
import scipy.stats
import scipy.optimize


# __Tab1 functions__

# In[49]:


def chart1_data_long_func(effect_uplift,
                            sample_stdev,
                            sample_size):
    ### Log-space parameters
    ### Using 1 as mu (basis point)
    H_null = 1
    H_alternative = 1 + effect_uplift
    lognormal_stdev = 1 + sample_stdev

    normal_H_null = np.log10(H_null)
    normal_H_alternative = np.log10(H_alternative)
    normal_stdev = np.log10(lognormal_stdev)

    test_result_raw = scipy.stats.ttest_ind_from_stats(mean1 = normal_H_null, std1 = normal_stdev,
                                                       nobs1 = np.round(sample_size / 2),
                                                       mean2 = normal_H_alternative, std2 = normal_stdev, 
                                                       nobs2 = np.round(sample_size / 2),
                                                       equal_var = True
                                                       )

    test_result_pvalue = test_result_raw[1]

    test_result_pvalue /= 2

    x1 = np.linspace(scipy.stats.lognorm.ppf(0.01, sample_stdev),
                     scipy.stats.lognorm.ppf(0.99, sample_stdev), 100)
    lognorm_pdf = scipy.stats.lognorm.pdf(x1, sample_stdev)

    n_per_sample = sample_size / 2
    ### independent 2-sample degrees of freedom
    dof = 2 * n_per_sample - 2 
    x2 = np.linspace(scipy.stats.t.ppf(0.01, df = dof, scale = normal_stdev),
                     scipy.stats.t.ppf(0.99, df = dof, scale = normal_stdev), 100)
    t_pdf = scipy.stats.t.pdf(x2, df = dof, scale = normal_stdev)
    test_statistic = normal_H_alternative / (normal_stdev * np.sqrt(2 / n_per_sample))

    data_dict_long = {"x1": x1,
                 "lognorm_pdf": lognorm_pdf,
                 "x2": x2,
                 "t_pdf": t_pdf
                 }
    
    data_dict_short = {"H_alternative": [H_alternative, H_alternative],
                 "min_max_lognorm": [np.min(lognorm_pdf), np.max(lognorm_pdf)],
                 "t_test_stat": [test_statistic * normal_stdev for i in range(2)],
                 "min_max_t_pdf": [np.min(t_pdf), np.max(t_pdf)]
                               }
    
    return data_dict_long


# In[50]:


def chart1_data_short_func(effect_uplift,
                            sample_stdev,
                            sample_size):
    ### Log-space parameters
    ### Using 1 as mu (basis point)
    H_null = 1
    H_alternative = 1 + effect_uplift
    lognormal_stdev = 1 + sample_stdev

    normal_H_null = np.log10(H_null)
    normal_H_alternative = np.log10(H_alternative)
    normal_stdev = np.log10(lognormal_stdev)

    test_result_raw = scipy.stats.ttest_ind_from_stats(mean1 = normal_H_null, std1 = normal_stdev,
                                                       nobs1 = np.round(sample_size / 2),
                                                       mean2 = normal_H_alternative, std2 = normal_stdev, 
                                                       nobs2 = np.round(sample_size / 2),
                                                       equal_var = True
                                                       )

    test_result_pvalue = test_result_raw[1]

    test_result_pvalue /= 2

    x1 = np.linspace(scipy.stats.lognorm.ppf(0.01, sample_stdev),
                     scipy.stats.lognorm.ppf(0.99, sample_stdev), 100)
    lognorm_pdf = scipy.stats.lognorm.pdf(x1, sample_stdev)

    n_per_sample = sample_size / 2
    ### independent 2-sample degrees of freedom
    dof = 2 * n_per_sample - 2 
    x2 = np.linspace(scipy.stats.t.ppf(0.01, df = dof, scale = normal_stdev),
                     scipy.stats.t.ppf(0.99, df = dof, scale = normal_stdev), 100)
    t_pdf = scipy.stats.t.pdf(x2, df = dof, scale = normal_stdev)
    test_statistic = normal_H_alternative / (normal_stdev * np.sqrt(2 / n_per_sample))

    data_dict_long = {"x1": x1,
                 "lognorm_pdf": lognorm_pdf,
                 "x2": x2,
                 "t_pdf": t_pdf
                 }
    
    data_dict_short = {"H_alternative": [H_alternative, H_alternative],
                 "min_max_lognorm": [np.min(lognorm_pdf), np.max(lognorm_pdf)],
                 "t_test_stat": [test_statistic * normal_stdev for i in range(2)],
                 "min_max_t_pdf": [np.min(t_pdf), np.max(t_pdf)]
                               }
    
    return data_dict_short


# In[51]:


def chart1_text_func(effect_uplift,
                     sample_stdev,
                     sample_size):
    ### Log-space parameters
    ### Using 1 as mu (basis point)
    H_null = 1
    H_alternative = 1 + effect_uplift
    lognormal_stdev = 1 + sample_stdev

    normal_H_null = np.log10(H_null)
    normal_H_alternative = np.log10(H_alternative)
    normal_stdev = np.log10(lognormal_stdev)

    test_result_raw = scipy.stats.ttest_ind_from_stats(mean1 = normal_H_null, std1 = normal_stdev,
                                                       nobs1 = np.round(sample_size / 2),
                                                       mean2 = normal_H_alternative, std2 = normal_stdev, 
                                                       nobs2 = np.round(sample_size / 2),
                                                       equal_var = True
                                                       )

    test_result_pvalue = test_result_raw[1]

    test_result_pvalue /= 2
    
    return {'x': [0], 'y': [0.25],
            'text': ["Test's pvalue: " + str(np.round(test_result_pvalue, 3)) +
                     "        (Confidence Level: " + 
                     str(np.round(100 * (1 - test_result_pvalue), 1)) + "%)"]}


# __Tab2 functions__

# In[52]:


def chart2_data_long_func(effect_uplift,
                          sample_stdev,
                          desired_percent_confidence):
    
    user_desired_pvalue = 1 - desired_percent_confidence

    H_null = 1
    H_alternative = 1 + effect_uplift
    lognormal_stdev = 1 + sample_stdev

    normal_H_null = np.log10(H_null)
    normal_H_alternative = np.log10(H_alternative)
    normal_stdev = np.log10(lognormal_stdev)
    
    ### optimize
    test_result_pvalue = 1
    n_per_sample = 2
    while test_result_pvalue > user_desired_pvalue and n_per_sample < 2000:
        test_result_raw = scipy.stats.ttest_ind_from_stats(mean1 = normal_H_null, std1 = normal_stdev,
                                                       nobs1 = n_per_sample,
                                                       mean2 = normal_H_alternative, std2 = normal_stdev, 
                                                       nobs2 = n_per_sample,
                                                       equal_var = True
                                                       )
        test_result_pvalue = test_result_raw[1]
    
        test_result_pvalue /= 2
        
        n_per_sample += 1
        
    
    x1 = np.linspace(scipy.stats.lognorm.ppf(0.01, sample_stdev),
                     scipy.stats.lognorm.ppf(0.99, sample_stdev), 100)
    lognorm_pdf = scipy.stats.lognorm.pdf(x1, sample_stdev)

    ### independent 2-sample degrees of freedom
    dof = 2 * n_per_sample - 2 
    x2 = np.linspace(scipy.stats.t.ppf(0.01, df = dof, scale = normal_stdev),
                     scipy.stats.t.ppf(0.99, df = dof, scale = normal_stdev), 100)
    t_pdf = scipy.stats.t.pdf(x2, df = dof, scale = normal_stdev)
    test_statistic = normal_H_alternative / (normal_stdev * np.sqrt(2 / n_per_sample))

    data_dict_long = {"x1": x1,
                      "lognorm_pdf": lognorm_pdf,
                      "x2": x2,
                      "t_pdf": t_pdf
                      }
    
    data_dict_short = {"H_alternative": [H_alternative, H_alternative],
                       "min_max_lognorm": [np.min(lognorm_pdf), np.max(lognorm_pdf)],
                       "t_test_stat": [test_statistic * normal_stdev for i in range(2)],
                       "min_max_t_pdf": [np.min(t_pdf), np.max(t_pdf)]
                       }
    
    return data_dict_long


# In[53]:


def chart2_data_short_func(effect_uplift,
                          sample_stdev,
                          desired_percent_confidence):
    
    user_desired_pvalue = 1 - desired_percent_confidence

    H_null = 1
    H_alternative = 1 + effect_uplift
    lognormal_stdev = 1 + sample_stdev

    normal_H_null = np.log10(H_null)
    normal_H_alternative = np.log10(H_alternative)
    normal_stdev = np.log10(lognormal_stdev)
    
    ### optimize
    test_result_pvalue = 1
    n_per_sample = 2
    while test_result_pvalue > user_desired_pvalue and n_per_sample < 2000:
        test_result_raw = scipy.stats.ttest_ind_from_stats(mean1 = normal_H_null, std1 = normal_stdev,
                                                       nobs1 = n_per_sample,
                                                       mean2 = normal_H_alternative, std2 = normal_stdev, 
                                                       nobs2 = n_per_sample,
                                                       equal_var = True
                                                       )
        test_result_pvalue = test_result_raw[1]
    
        test_result_pvalue /= 2
        
        n_per_sample += 1
        
    
    x1 = np.linspace(scipy.stats.lognorm.ppf(0.01, sample_stdev),
                     scipy.stats.lognorm.ppf(0.99, sample_stdev), 100)
    lognorm_pdf = scipy.stats.lognorm.pdf(x1, sample_stdev)

    ### independent 2-sample degrees of freedom
    dof = 2 * n_per_sample - 2 
    x2 = np.linspace(scipy.stats.t.ppf(0.01, df = dof, scale = normal_stdev),
                     scipy.stats.t.ppf(0.99, df = dof, scale = normal_stdev), 100)
    t_pdf = scipy.stats.t.pdf(x2, df = dof, scale = normal_stdev)
    test_statistic = normal_H_alternative / (normal_stdev * np.sqrt(2 / n_per_sample))

    data_dict_long = {"x1": x1,
                      "lognorm_pdf": lognorm_pdf,
                      "x2": x2,
                      "t_pdf": t_pdf
                      }
    
    data_dict_short = {"H_alternative": [H_alternative, H_alternative],
                       "min_max_lognorm": [np.min(lognorm_pdf), np.max(lognorm_pdf)],
                       "t_test_stat": [test_statistic * normal_stdev for i in range(2)],
                       "min_max_t_pdf": [np.min(t_pdf), np.max(t_pdf)]
                       }
    
    return data_dict_short


# In[54]:


def chart2_text_func(effect_uplift,
                     sample_stdev,
                     desired_percent_confidence):
    
    user_desired_pvalue = 1 - desired_percent_confidence

    H_null = 1
    H_alternative = 1 + effect_uplift
    lognormal_stdev = 1 + sample_stdev

    normal_H_null = np.log10(H_null)
    normal_H_alternative = np.log10(H_alternative)
    normal_stdev = np.log10(lognormal_stdev)
    
    ### optimize
    test_result_pvalue = 1
    n_per_sample = 2
    while test_result_pvalue > user_desired_pvalue and n_per_sample < 2000:
        test_result_raw = scipy.stats.ttest_ind_from_stats(mean1 = normal_H_null, std1 = normal_stdev,
                                                       nobs1 = n_per_sample,
                                                       mean2 = normal_H_alternative, std2 = normal_stdev, 
                                                       nobs2 = n_per_sample,
                                                       equal_var = True
                                                       )
        test_result_pvalue = test_result_raw[1]
    
        test_result_pvalue /= 2
        
        n_per_sample += 1
        
    
    return {'x': [0], 'y': [0.25],
            'text': ["Number wells needed per sample (half the pilot): " + str(n_per_sample)]}


# __Data Sources__

# In[55]:


chart1_data_long = bokeh.models.ColumnDataSource(data = 
                                                   chart1_data_long_func(effect_uplift = 0.03,
                                                                           sample_stdev = 0.1,
                                                                           sample_size = 6))

chart1_data_short = bokeh.models.ColumnDataSource(data = 
                                                   chart1_data_short_func(effect_uplift = 0.03,
                                                                           sample_stdev = 0.1,
                                                                           sample_size = 6))

source_text1 = bokeh.models.ColumnDataSource(data = chart1_text_func(effect_uplift = 0.03,
                                                                     sample_stdev = 0.1,
                                                                     sample_size = 6))


# In[56]:


chart2_data_long = bokeh.models.ColumnDataSource(data = 
                                                   chart2_data_long_func(effect_uplift = 0.03,
                                                                           sample_stdev = 0.1,
                                                                           desired_percent_confidence = 0.9))

chart2_data_short = bokeh.models.ColumnDataSource(data = 
                                                   chart2_data_short_func(effect_uplift = 0.03,
                                                                           sample_stdev = 0.1,
                                                                           desired_percent_confidence = 0.9))

source_text2 = bokeh.models.ColumnDataSource(data = chart2_text_func(effect_uplift = 0.03,
                                                                     sample_stdev = 0.1,
                                                                     desired_percent_confidence = 0.9))


# __Sliders__

# In[57]:


percent_uplift_slider = bokeh.models.widgets.Slider(start = 1, end = 100, value = 3,
                                                    step = 1, title = "% Uplift",
                                           width = 400)

st_dev_as_percent_of_mean_slider = bokeh.models.widgets.Slider(start = 1, end = 100, value = 10, step = 1, 
                                                               title = "St Dev as % of Mean",
                                           width = 400)

sample_size_slider = bokeh.models.widgets.Slider(start = 4, end = 50, value = 4, step = 2, 
                                                 title = "Total Number Wells Across Both Groups",
                                           width = 400)

seek_p_desired_percent_confidence_slider = bokeh.models.widgets.Slider(start = 51, end = 99, value = 90, step = 1, 
                                                 title = "Desired % Confidence (Single, Right-Tailed)",
                                           width = 400)



seek_p_percent_uplift_slider = bokeh.models.widgets.Slider(start = 1, end = 100, value = 3,
                                                    step = 1, title = "% Uplift",
                                           width = 400)

seek_p_st_dev_as_percent_of_mean_slider = bokeh.models.widgets.Slider(start = 1, end = 100, value = 10, step = 1, 
                                                               title = "St Dev as % of Mean",
                                           width = 400)


# https://stackoverflow.com/questions/50499390/bokeh-how-to-have-the-same-widget-or-duplicate-a-widget-in-two-different-tab

# In[58]:


def link_property(property_name, *widgets):
    wb = bokeh.layouts.widgetbox(*widgets)

    wb.tags = [property_name, 0]
    def callback(widgets=wb):
        if widgets.tags[1] != 0:
            return
        widgets.tags[1] = 1
        for widget in widgets.children:
            widget[widgets.tags[0]] = cb_obj.value
        widgets.tags[1] = 0

    jscallback = bokeh.models.CustomJS.from_py_func(callback)

    for widget in widgets:
        widget.js_on_change(property_name, jscallback)
        
link_property("value", percent_uplift_slider, seek_p_percent_uplift_slider) 
link_property("value", seek_p_st_dev_as_percent_of_mean_slider, st_dev_as_percent_of_mean_slider) 


# __Callbacks__

# In[59]:


def callback_chart1(attr, old, new):
    percent_uplift_slider_value = percent_uplift_slider.value / 100
    st_dev_as_percent_of_mean_slider_value = st_dev_as_percent_of_mean_slider.value / 100
    sample_size_slider_value = sample_size_slider.value
    
    chart1_data_long.data = chart1_data_long_func(effect_uplift = percent_uplift_slider_value,
                                            sample_stdev = st_dev_as_percent_of_mean_slider_value,
                                            sample_size = sample_size_slider_value)
    chart1_data_short.data = chart1_data_short_func(effect_uplift = percent_uplift_slider_value,
                                            sample_stdev = st_dev_as_percent_of_mean_slider_value,
                                            sample_size = sample_size_slider_value)
    source_text1.data = chart1_text_func(effect_uplift = percent_uplift_slider_value,
                                            sample_stdev = st_dev_as_percent_of_mean_slider_value,
                                            sample_size = sample_size_slider_value)    

    seek_p_desired_percent_confidence_slider_value = seek_p_desired_percent_confidence_slider.value / 100
    
    chart2_data_long.data = chart2_data_long_func(effect_uplift = percent_uplift_slider_value,
                                            sample_stdev = st_dev_as_percent_of_mean_slider_value,
                                            desired_percent_confidence = seek_p_desired_percent_confidence_slider_value)
    chart2_data_short.data = chart2_data_short_func(effect_uplift = percent_uplift_slider_value,
                                            sample_stdev = st_dev_as_percent_of_mean_slider_value,
                                            desired_percent_confidence = seek_p_desired_percent_confidence_slider_value)
    source_text2.data = chart2_text_func(effect_uplift = percent_uplift_slider_value,
                                            sample_stdev = st_dev_as_percent_of_mean_slider_value,
                                            desired_percent_confidence = seek_p_desired_percent_confidence_slider_value)    
    
percent_uplift_slider.on_change('value', callback_chart1)
st_dev_as_percent_of_mean_slider.on_change('value', callback_chart1)
sample_size_slider.on_change('value', callback_chart1)
seek_p_desired_percent_confidence_slider.on_change('value', callback_chart1)


# In[60]:


text_plot1 = bokeh.plotting.figure(plot_width=800, plot_height=25,
                                 min_border=0, toolbar_location=None)
text_plot1.x_range = bokeh.models.ranges.Range1d(0, 1, bounds = 'auto')
text_plot1.y_range = bokeh.models.ranges.Range1d(0, 1, bounds = 'auto')
text_plot1.xgrid.grid_line_color = None
text_plot1.ygrid.grid_line_color = None
text_plot1.xaxis.visible = False
text_plot1.yaxis.visible = False
#text_plot1.xaxis.axis_line_color = None
#text_plot1.yaxis.axis_line_color = None
text_plot1.add_glyph(source_text1,
                     bokeh.models.glyphs.Text(x="x", y="y", text="text", angle=0))


# In[61]:


p_left1 = bokeh.plotting.figure(x_axis_label = "Performance Shift Away from 100%",
                                y_axis_label = "Well Performance Probability Density",
                                title = "Lognormal Well Distribution",
                                plot_width=400, plot_height=400)

p_left1.line('x1', 'lognorm_pdf', source = chart1_data_long, line_width = 2, color = 'navy')
p_left1.line('H_alternative', 'min_max_lognorm', source = chart1_data_short, line_width = 2, color = 'firebrick')

p_right1 = bokeh.plotting.figure(x_axis_label = "Normalized Performance Shift",
                                y_axis_label = "Well Performance Probability Density",
                                 title = "Normalized, Student-T Well Distribution",
                                 plot_width=400, plot_height=400)

p_right1.line('x2', 't_pdf', source = chart1_data_long, line_width = 2, color = 'navy')
p_right1.line('t_test_stat', 'min_max_t_pdf', source = chart1_data_short, line_width = 2, color = 'firebrick')


# __second plots__

# In[62]:


text_plot2 = bokeh.plotting.figure(plot_width=800, plot_height=25,
                                 min_border=0, toolbar_location=None)
text_plot2.x_range = bokeh.models.ranges.Range1d(0, 1, bounds = 'auto')
text_plot2.y_range = bokeh.models.ranges.Range1d(0, 1, bounds = 'auto')
text_plot2.xgrid.grid_line_color = None
text_plot2.ygrid.grid_line_color = None
text_plot2.xaxis.visible = False
text_plot2.yaxis.visible = False
#text_plot2.xaxis.axis_line_color = None
#text_plot2.yaxis.axis_line_color = None
text_plot2.add_glyph(source_text2,
                     bokeh.models.glyphs.Text(x="x", y="y", text="text", angle=0))


# In[63]:


p_left2 = bokeh.plotting.figure(x_axis_label = "Performance Shift Away from 100%",
                                y_axis_label = "Well Performance Probability Density",
                                title = "Lognormal Well Distribution",
                                plot_width=400, plot_height=400)

p_left2.line('x1', 'lognorm_pdf', source = chart2_data_long, line_width = 2, color = 'navy')
p_left2.line('H_alternative', 'min_max_lognorm', source = chart2_data_short, line_width = 2, color = 'firebrick')

p_right2 = bokeh.plotting.figure(x_axis_label = "Normalized Performance Shift",
                                y_axis_label = "Well Performance Probability Density",
                                 title = "Normalized, Student-T Well Distribution",
                                 plot_width=400, plot_height=400)

p_right2.line('x2', 't_pdf', source = chart2_data_long, line_width = 2, color = 'navy')
p_right2.line('t_test_stat', 'min_max_t_pdf', source = chart2_data_short, line_width = 2, color = 'firebrick')


# __setup tabs__

# In[79]:


first_panel = bokeh.models.widgets.Panel(child = bokeh.layouts.layout([percent_uplift_slider,
                      st_dev_as_percent_of_mean_slider,
                      sample_size_slider,
                      text_plot1,
                      [p_left1, p_right1]], text_font_style = 'bold'),
                           title = 'Given Well Count, Get Confidence')


# In[80]:


second_panel = bokeh.models.widgets.Panel(child = bokeh.layouts.layout([seek_p_percent_uplift_slider,
                                                 seek_p_st_dev_as_percent_of_mean_slider,
                                                 seek_p_desired_percent_confidence_slider,
                                                 text_plot2,
                                                 [p_left2, p_right2]], text_font_style = 'bold'),
                           title = 'Given Confidence, Get Well Count')


# In[84]:


tabs = bokeh.models.widgets.Tabs(tabs = [first_panel, second_panel])


# In[85]:


bokeh.io.curdoc().add_root(tabs)


# In[ ]:




