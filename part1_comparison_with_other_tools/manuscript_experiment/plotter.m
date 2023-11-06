
memories = [15.474451171875 32.13496875 47.1231767578125 64.7082021484375 80.60047558593749 
12.762083007812501 29.408337890625 43.8183291015625 57.265997070312494 67.42272460937498 
12.642191406250001 27.714394531249997 40.6554931640625 52.30454296875 63.90098437499999];

meories_error = [1.6771329896464617 1.4624015779800275 4.986660718686601 0.36367639816732894 0.4489181975641962 
0.44409146296566077 2.2411693070148067 1.7665847650077358 0.8699335116975963 1.4873306800836272 
1.9650838952061351 2.099529020192009 0.7011823900408739 2.4994344231339367 2.608778003459343 ];

category_names = {'2M', '4M', '6M', '8M', '10M'};

Y = memories';
Y_er = meories_error';
cat_label = categorical(category_names); %The Group Label
cat_label = reordercats(cat_label,category_names);%To Preserve Label Order
b = bar(Y,'grouped', 'BarWidth', 1.0);

set(gcf, 'units', 'inch', 'position',[0, 0, 5, 3]);
set(gca, 'FontName', 'Arial');
hold on;
grid on;
% Calculate the number of groups and number of bars in each group
[ngroups,nbars] = size(Y);
% Get the x coordinate of the bars
x = nan(nbars, ngroups);
for i = 1:nbars
    x(i,:) = b(i).XEndPoints;
end
errorbar(x',Y,Y_er,'k','linestyle','none','LineWidth', 0.9);%Adding the errorbars
hold off
set(gca,'xticklabel',cat_label);
legend('Diamond', 'sourmash, k=11', 'sourmash, k=15', 'Location', 'northoutside', 'Fontsize', 8);

%title('Memory usage', 'FontSize', 11);
xlabel('Number of reads in metagenome', 'FontSize', 9);
ylabel('Average memory usage (GB)', 'FontSize', 9);

set(gcf, 'PaperUnits', 'inches');
set(gcf, 'PaperSize', [5 3]);
print(gcf, 'large_MGs_memory.pdf', '-dpdf', '-bestfit');

%%

times = [3.952505334414095 4.229146373780905 4.398058096977327 4.52986328905765 4.61563279778133 
2.314145630024391 2.6199848200583298 2.7606487134818054 2.8552888336793005 2.9262171276157476 
2.2877409090520753 2.5993392238444537 2.7388198657895435 2.8300136980439423 2.908300721486597];

times_error = [0.01786696059073064 0.017615553298760293 0.015303129553673833 0.0044527605168704415 0.01462879114302703 
0.01871597650427767 0.019526183366307383 0.009508540005907118 0.0007780972514998738 0.006932913959106646 
0.031318829716757084 0.017564254502681106 0.004082516828665632 0.009241991530398166 0.006771054224015415 ];

category_names = {'2M', '4M', '6M', '8M', '10M'};

Y = times';
Y_er = times_error';
cat_label = categorical(category_names); %The Group Label
cat_label = reordercats(cat_label,category_names);%To Preserve Label Order
b = bar(Y,'grouped', 'BarWidth', 1.0);

set(gcf, 'units', 'inch', 'position',[0, 0, 5, 3]);
set(gca, 'FontName', 'Arial');
hold on;
grid on;
% Calculate the number of groups and number of bars in each group
[ngroups,nbars] = size(Y);
% Get the x coordinate of the bars
x = nan(nbars, ngroups);
for i = 1:nbars
    x(i,:) = b(i).XEndPoints;
end
errorbar(x',Y,Y_er,'k','linestyle','none','LineWidth', 0.9);%Adding the errorbars
hold off
set(gca,'xticklabel',cat_label);
legend('Diamond', 'sourmash, k=11', 'sourmash, k=15', 'Location', 'northoutside', 'Fontsize', 8);

%title('Running time for identifying KOs by various approaches', 'FontSize', 11);
xlabel('Number of reads in metagenome', 'FontSize', 9);
ylabel('Avg CPU time (seconds)', 'FontSize', 9);
yticklabels({'10^0', '10^1', '10^2', '10^3', '10^4', '10^5'})

set(gcf, 'PaperUnits', 'inches');
set(gcf, 'PaperSize', [5 3]);
print(gcf, 'large_MGs_runtime.pdf', '-dpdf', '-bestfit');

%%

f1s = [0.8847301712742383 0.8880619749489485 0.8896259142881779 0.8908775978321698 0.8905484084161788
0.8432734149969336 0.8684417027831037 0.8887103544491444 0.8952142981548598 0.8990073275891041
0.8363578700417402 0.8720934905977167 0.8891791996209022 0.8916305708625766 0.9000452651024572 ];

f1s_error = [0.005273069453116441 0.005443651305338725 0.006142412153790997 0.006079503730739759 0.006966635807099837
0.0038639536500277806 0.0025908049368146965 0.0031997973665810675 0.004144013850516707 0.0029998614429398445
0.0037075740342993333 0.0017204188022984282 0.0017140448805185904 0.0026591063615494237 0.001627776636061025 ];

category_names = {'2M', '4M', '6M', '8M', '10M'};

Y = f1s'*100;
Y_er = f1s_error'*100;
cat_label = categorical(category_names); %The Group Label
cat_label = reordercats(cat_label,category_names);%To Preserve Label Order
b = bar(Y,'grouped', 'BarWidth', 1.0);

set(gcf, 'units', 'inch', 'position',[0, 0, 5, 3]);
set(gca, 'FontName', 'Arial');
hold on;
grid on;
% Calculate the number of groups and number of bars in each group
[ngroups,nbars] = size(Y);
% Get the x coordinate of the bars
x = nan(nbars, ngroups);
for i = 1:nbars
    x(i,:) = b(i).XEndPoints;
end
errorbar(x',Y,Y_er,'k','linestyle','none', 'LineWidth', 0.9);%Adding the errorbars
hold off
set(gca,'xticklabel',cat_label);
legend('Diamond', 'sourmash, k=11', 'sourmash, k=15', 'Location', 'northoutside', 'Fontsize', 8);
%title('F1 scores in identifying KOs by various approaches', 'FontSize', 11);
xlabel('Number of reads in metagenome', 'FontSize', 9);
ylabel('Average F1 score', 'FontSize', 9);

set(gcf, 'PaperUnits', 'inches');
set(gcf, 'PaperSize', [5 3]);
print(gcf, 'large_MGs_F1.pdf', '-dpdf', '-bestfit');

%%

recalls = [0.8691224800254214 0.8714762695154663 0.873877180607319 0.8753224108870136 0.8751047462412679
0.793539213187585 0.9121977865442167 0.899407507417639 0.8866392604270988 0.91049247237624
0.7874706242388564 0.9037782212891011 0.8895108869425797 0.9040660521954076 0.9040838972720966 ];

recalls_error = [0.011528227853333364 0.01019371743486841 0.01029700585794212 0.01076347223974885 0.010755326320193841
0.006535672467911275 0.0030578463378402314 0.006332341111502415 0.012983668041781337 0.0062331479948933175
0.04071468008873657 0.0045798766548551745 0.002552073337471258 0.02703456743527988 0.0024697565980176814];

category_names = {'2M', '4M', '6M', '8M', '10M'};

Y = recalls'*100;
Y_er = recalls_error'*100;
cat_label = categorical(category_names); %The Group Label
cat_label = reordercats(cat_label,category_names);%To Preserve Label Order
b = bar(Y,'grouped', 'BarWidth', 1.0);

set(gcf,'units', 'inch', 'position',[0, 0, 5, 3]);
set(gca, 'FontName', 'Arial');
hold on
grid on
% Calculate the number of groups and number of bars in each group
[ngroups,nbars] = size(Y);
% Get the x coordinate of the bars
x = nan(nbars, ngroups);
for i = 1:nbars
    x(i,:) = b(i).XEndPoints;
end
errorbar(x',Y,Y_er,'k','linestyle','none', 'LineWidth', 0.9);%Adding the errorbars
hold off
set(gca,'xticklabel',cat_label);
legend('Diamond', 'sourmash, k=11', 'sourmash, k=15', 'Location', 'northoutside', 'Fontsize', 8);
%title('Recalls (completeness scores) in identifying KOs by various approaches', 'FontSize', 11);
xlabel('Number of reads in metagenome', 'FontSize', 9);
ylabel('Average completeness', 'FontSize', 9);

set(gcf, 'PaperUnits', 'inches');
set(gcf, 'PaperSize', [5, 3]);
print(gcf, 'large_MGs_recall.pdf', '-dpdf', '-bestfit');

%%

precisions = [0.9011350055893483 0.9054644057096011 0.9061343942328219 0.9071795220328471 0.9067190486855352
0.8996985661424658 0.8287075577267649 0.8783021392064526 0.9045022083606827 0.8878516411869238
0.8965895227312869 0.8425830140345258 0.8888569787220236 0.8813594438026293 0.896050692325673];

precisions_error = [0.010674823670584244 0.010133839599430193 0.011211439705071718 0.010764946317963013 0.011374969061685676
0.003108252546158766 0.004257747239165635 0.0038705009494054868 0.018369574193220283 0.0044307572388060535
0.04431682251400676 0.0034439108912748084 0.002752404068744034 0.030872057487310513 0.002565605671598089];

%category_names = {'1M', '2M', '3M', '4M', '5M', '6M', '7M', '8M', '9M', '10M'};
category_names = {'2M', '4M', '6M', '8M', '10M'};

Y = precisions'*100;
Y_er = precisions_error'*100;
cat_label = categorical(category_names); %The Group Label
cat_label = reordercats(cat_label,category_names);%To Preserve Label Order
b = bar(Y,'grouped', 'BarWidth', 1.0);

set(gcf, 'units', 'inch', 'position',[0, 0, 5, 3]);
set(gca, 'FontName', 'Arial');
hold on;
grid on;
% Calculate the number of groups and number of bars in each group
[ngroups,nbars] = size(Y);
% Get the x coordinate of the bars
x = nan(nbars, ngroups);
for i = 1:nbars
    x(i,:) = b(i).XEndPoints;
end
errorbar(x',Y,Y_er,'k','linestyle','none', 'LineWidth', 0.9);%Adding the errorbars
hold off;
set(gca,'xticklabel',cat_label);
legend('Diamond', 'sourmash, k=11', 'sourmash, k=15', 'Location', 'northoutside', 'Fontsize', 8);
%title('Precisions (purity scores) in identifying KOs by various tools', 'FontSize', 11);
xlabel('Number of reads in metagenome', 'FontSize', 9);
ylabel('Average purity', 'FontSize', 9);

set(gcf, 'PaperUnits', 'inches');
set(gcf, 'PaperSize', [5 3]);
print(gcf, 'large_MGs_precision.pdf', '-dpdf', '-bestfit');
%%

times = [1.9281081992747524 2.005597142347061 2.0142350736943704 2.157398243822439 2.130168818408767
1.0134620812097483 1.0084988314290126 0.9730169353069114 1.014872874507723 1.0297368830166767 
0.9810852033310182 1.0115995397738162 0.9697642196628193 1.0133565378510754 1.020356512236863
2.810238570195133 2.8843570827217566 3.1011531328342308 3.270920925508024 3.296401143614665 ];

times_error = [0.0694046620324682 0.05345969811128431 0.05826469016163988 0.0734978495012771 0.07584186716120868
0.06403489674112783 0.05836348009931109 0.08070288794209939 0.05167967117276125 0.020746026668425795 
0.06530733185603799 0.044328840335494946 0.06003893053356753 0.07210225436396077 0.03725488156371673
0.08851132296414017 0.11010172688151021 0.07197504831376413 0.12432980525825636 0.1480338660339257 ];

category_names = { '10K' '20K' '30K' '40K' '50K'};

Y = times';
Y_er = times_error';
cat_label = categorical(category_names); %The Group Label
cat_label = reordercats(cat_label,category_names);%To Preserve Label Order
b = bar(Y,'grouped', 'BarWidth', 1.0);

set(gcf, 'units', 'inch', 'position',[0, 0, 5, 3]);
set(gca, 'FontName', 'Arial');
hold on;
grid on;
% Calculate the number of groups and number of bars in each group
[ngroups,nbars] = size(Y);
% Get the x coordinate of the bars
x = nan(nbars, ngroups);
for i = 1:nbars
    x(i,:) = b(i).XEndPoints;
end
errorbar(x',Y,Y_er,'k','linestyle','none','LineWidth', 0.9);%Adding the errorbars
hold off
set(gca,'xticklabel',cat_label);
legend('Diamond', 'sourmash, k=11', 'sourmash, k=15', 'KofamScan', 'Location', 'northoutside', 'Fontsize', 8, 'NumColumns', 2);

%title('Running time for identifying KOs by various approaches', 'FontSize', 11);
xlabel('Number of reads in metagenome', 'FontSize', 9);
ylabel('Avg. runtime (seconds)', 'FontSize', 9);

yticklabels({'10^0', '10^1', '10^2', '10^3'});

set(gcf, 'PaperUnits', 'inches');
set(gcf, 'PaperSize', [5 3]);
print(gcf, 'small_MGs_runtime.pdf', '-dpdf', '-bestfit');

%%

f1s = [0.7036103948576978 0.7750977946410245 0.8065375467856569 0.8272762809240822 0.794818578441277
0.1997364059578411 0.25238766057469414 0.2896984005724397 0.31939008790471546 0.3937483813999844
0.18358623382030134 0.2268316072312288 0.2637787404262069 0.29542851452401153 0.3672372021854116
0.014290895683581661 0.02121512500710925 0.025042427877745126 0.02834185370620713 0.03193758720333386 ];

f1s_error = [0.019247904066787138 0.014640266526369905 0.013559560234084255 0.012015689581233762 0.007837503989119202
0.017668189310268933 0.017980598490932732 0.012186090592529222 0.010234158477759051 0.009649142750823812
0.015511026660934357 0.01219650384076225 0.008804692325919967 0.010042667254320263 0.011989286884239198
0.0032262319756699814 0.0024126439802736074 0.0030083131752483535 0.0025064640304727093 0.0024522811649590097 ];

category_names = { '10K' '20K' '30K' '40K' '50K'};

Y = f1s'*100;
Y_er = f1s_error'*100;
cat_label = categorical(category_names); %The Group Label
cat_label = reordercats(cat_label,category_names);%To Preserve Label Order
b = bar(Y,'grouped', 'BarWidth', 1.0);

set(gcf, 'units', 'inch', 'position',[0, 0, 5, 3]);
set(gca, 'FontName', 'Arial');
hold on;
grid on;
% Calculate the number of groups and number of bars in each group
[ngroups,nbars] = size(Y);
% Get the x coordinate of the bars
x = nan(nbars, ngroups);
for i = 1:nbars
    x(i,:) = b(i).XEndPoints;
end
errorbar(x',Y,Y_er,'k','linestyle','none', 'LineWidth', 0.9);%Adding the errorbars
hold off
set(gca,'xticklabel',cat_label);
legend('Diamond', 'sourmash, k=11', 'sourmash, k=15', 'KofamScan', 'Location', 'northoutside', 'Fontsize', 8, 'NumColumns', 2);
%title('F1 scores in identifying KOs by various approaches', 'FontSize', 11);
xlabel('Number of reads in simulated metagenome', 'FontSize', 9);
ylabel('Average F1 score', 'FontSize', 9);

set(gcf, 'PaperUnits', 'inches');
set(gcf, 'PaperSize', [5 3]);
print(gcf, 'small_MGs_F1.pdf', '-dpdf', '-bestfit');

%%

recalls = [0.669718077301596 0.7342472633580487 0.7647353678649813 0.7873912560463041 0.76482316780426
0.11490781795552671 0.14796113780781434 0.17262019784479093 0.19311147917856647 0.25443297092324124
0.10436799162005853 0.13061002145703607 0.15452799712562032 0.17588597544196743 0.23255180689589147
0.008469368077915243 0.01227839457834251 0.014391208473335002 0.016260793171863873 0.019007919922406517];

recalls_error = [0.030033170734385214 0.026906765225247587 0.025480281029699542 0.024494043055033964 0.013640216437979686
0.010902120379453317 0.011871390904064982 0.008315976013053365 0.007309673849755055 0.007952213489643246
0.009692220881452704 0.007879202728263432 0.005951260319952497 0.007101944558611059 0.009505979578359684
0.0019522401706521893 0.0013877906382439274 0.0017545639874055503 0.0014934348329733109 0.0015221929353096408 ];

category_names = { '10K' '20K' '30K' '40K' '50K'};

Y = recalls'*100;
Y_er = recalls_error'*100;
cat_label = categorical(category_names); %The Group Label
cat_label = reordercats(cat_label,category_names);%To Preserve Label Order
b = bar(Y,'grouped', 'BarWidth', 1.0);

x0 = 10;
y0 = 10;
width = 1200;
height = 400;
set(gcf,'units', 'inch', 'position',[0, 0, 5, 3]);
set(gca, 'FontName', 'Arial');
hold on
grid on
% Calculate the number of groups and number of bars in each group
[ngroups,nbars] = size(Y);
% Get the x coordinate of the bars
x = nan(nbars, ngroups);
for i = 1:nbars
    x(i,:) = b(i).XEndPoints;
end
errorbar(x',Y,Y_er,'k','linestyle','none', 'LineWidth', 0.9);%Adding the errorbars
hold off
set(gca,'xticklabel',cat_label);
legend('Diamond', 'sourmash, k=11', 'sourmash, k=15', 'KofamScan', 'Location', 'northoutside', 'Fontsize', 8, 'NumColumns', 2);
%title('Recalls (completeness scores) in identifying KOs by various approaches', 'FontSize', 11);
xlabel('Number of reads in simulated metagenome', 'FontSize', 9);
ylabel('Average completeness', 'FontSize', 9);

set(gcf, 'PaperUnits', 'inches');
set(gcf, 'PaperSize', [5 3]);
print(gcf, 'small_MGs_recall.pdf', '-dpdf', '-bestfit');

%%

precisions = [0.7417879179060136 0.8214159839308645 0.8537830842021454 0.8720237698407498 0.8274949154943675
0.765660239040467 0.861150406807198 0.901623599749588 0.9237961719654179 0.8708848310725305
0.7661098374289097 0.8636211918136146 0.9013184660368484 0.9235935963572557 0.8737953342700923
0.04585063519560459 0.0781185741415548 0.0966555408860019 0.11059268918501355 0.1000815732242107 ];

precisions_error = [0.0111497501156853 0.005830455216506708 0.007147569704363173 0.0069073344555911215 0.009772115402133309
0.03952365812955189 0.018482604409739496 0.013272566961019232 0.008786229050851989 0.005751064411028851
0.028336072519777787 0.011606443196017476 0.008109538634984974 0.00956821836612765 0.00776196777357763
0.009466610564050564 0.009843155719145362 0.01141928594065853 0.008797403105098753 0.007078576384421362 ];

category_names = { '10K' '20K' '30K' '40K' '50K'};

Y = precisions'*100;
Y_er = precisions_error'*100;
cat_label = categorical(category_names); %The Group Label
cat_label = reordercats(cat_label,category_names);%To Preserve Label Order
b = bar(Y,'grouped', 'BarWidth', 1.0);

set(gcf, 'units', 'inch', 'position',[0, 0, 5, 3]);
set(gca, 'FontName', 'Arial');
hold on;
grid on;
% Calculate the number of groups and number of bars in each group
[ngroups,nbars] = size(Y);
% Get the x coordinate of the bars
x = nan(nbars, ngroups);
for i = 1:nbars
    x(i,:) = b(i).XEndPoints;
end
errorbar(x',Y,Y_er,'k','linestyle','none', 'LineWidth', 0.9);%Adding the errorbar
hold off;
set(gca,'xticklabel',cat_label);
legend('Diamond', 'sourmash, k=11', 'sourmash, k=15', 'KofamScan', 'Location', 'northoutside', 'Fontsize', 8, 'NumColumns', 2);
%title('Precisions (purity scores) in identifying KOs by various tools', 'FontSize', 11);
xlabel('Number of reads in metagenome', 'FontSize', 9);
ylabel('Average purity', 'FontSize', 9);

set(gcf, 'PaperUnits', 'inches');
set(gcf, 'PaperSize', [5 3]);
print(gcf, 'small_MGs_precision.pdf', '-dpdf', '-bestfit');

%%
memories = [5.9491298828125 6.1965478515625 6.6535048828125 7.7702880859375 7.130114257812501 
0.001 0.003 0.005 0.0124267578125 0.0495556640625 
0.001 0.003 0.005 0.018765625 0.024819335937500003
0.4626083984374999 0.593201171875 0.775306640625 0.8631181640625 1.0842841796875 ];

meories_error = [1.4905613537103028 0.9097874133228497 0.4732348353630898 0.978617945421153 0.9219428126029695  
0.0 0.0 0.0 0.02485351648836565 0.024778133951667343 
0.0 0.0 0.0 0.028669423576976286 0.030397655076011672
0.0560115021150011 0.09427716731309237 0.2015409120907425 0.1570877652505174 0.12633986615767337];

category_names = { '10K' '20K' '30K' '40K' '50K'};

Y = memories';
Y_er = meories_error';
cat_label = categorical(category_names); %The Group Label
cat_label = reordercats(cat_label,category_names);%To Preserve Label Order
b = bar(Y,'grouped', 'BarWidth', 1.0);

set(gcf, 'units', 'inch', 'position',[0, 0, 5, 3]);
set(gca, 'FontName', 'Arial');
hold on;
grid on;
% Calculate the number of groups and number of bars in each group
[ngroups,nbars] = size(Y);
% Get the x coordinate of the bars
x = nan(nbars, ngroups);
for i = 1:nbars
    x(i,:) = b(i).XEndPoints;
end
errorbar(x',Y,Y_er,'k','linestyle','none','LineWidth', 0.9);%Adding the errorbars
hold off
set(gca,'xticklabel',cat_label);
legend('Diamond', 'sourmash, k=11', 'sourmash, k=15', 'KofamScan', 'Location', 'northoutside', 'Fontsize', 8, 'NumColumns', 2);

%title('Memory usage', 'FontSize', 11);
xlabel('Number of reads in metagenome', 'FontSize', 9);
ylabel('Avg. memory usage (GB)', 'FontSize', 9);
ylim([0 15]);

set(gcf, 'PaperUnits', 'inches');
set(gcf, 'PaperSize', [5 3]);
print(gcf, 'small_MGs_memory.pdf', '-dpdf', '-bestfit');
