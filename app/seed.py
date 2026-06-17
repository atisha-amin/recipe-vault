"""
seed.py — Seed the database with all recipes from the Recipe Book.

This file is auto-generated from the Word document via the parser.
Run directly:  python -m app.seed
"""

from app.database import init_db
from app.recipes import add_recipe, get_all_recipes


RECIPES: list[dict] = [
    {
        "title": 'Carrot Cake',
        "category": 'Cakes',
        "source": 'Inspired by Dorie Greenspan’s Carrot Cake from NYT Cooking',
        "tags": ['vanilla', 'pear', 'carrot', 'cinnamon', 'cream cheese', 'coconut'],
        "ingredients": """--- INGREDIENTS – FOR THE CAKE ---
2 cups all-purpose flour
2 tsp. baking powder
2 tsp. baking soda
2 tsp. ground cinnamon
1 tsp. salt
¼ tsp. ground clove
¼ tsp. ground ginger
3-4 cups grated carrots (about 8-9 carrots-grated in fine cheese shredder)
½ to 1 cup chopped walnuts
2 cups brown sugar, packed
1 cup canola oil (or any flavorless oil)
4 large eggs, room temperature
--- For the Cream cheese Frosting ---
2-8 oz cream cheese bricks, chilled from fridge
1 cup (2 sticks) unsalted butter, room temperature
2-3 cups powdered sugar (used about 2.5 cups and worked well)
1 tablespoon vanilla extract
1⁄8 tsp. (generous pinch) salt
--- FOr Toppings ---
Chopped walnuts and/or toasted sweetened coconut flakes""",
        "instructions": """Preheat the oven to 325 degrees. Butter and flour two 9-inch round, 2-inch deep cake pans,
Whisk together the flour, cinnamon, ground ginger, ground clove, baking powder, baking soda and salt in medium bowl and set aside.
In a large bowl, whisk oil and sugar together. Then add in egg one by one until nice and smooth. Then in the same bowl, add in carrots and nuts and mix well (beat with mixture on low speed very slightly).
Using a large rubber spatula gently stir in the flour mixture to the mixture above really gently until just combined. Don’t overmix (stop as soon as all the flour disappears).
Divide into pans and bake for 32-33 mins (on bottom rack was fine for me. Can also switch racks at 16 mins if desired / prevent bottom from browning or drying out too much).
Let pan sit on counter for about 5 mins then transfer to cooling rack. Cool for about 20-30 mins before frosting! (Optional: At this point, the cakes can be wrapped airtight and kept at room temperature overnight or frozen for up to 2 months; thaw before frosting.)
Cream together butter and cream cheese until well combined. Add in powdered sugar slowly (will look soft / smooth / velvety), vanilla, and salt until well combined.""",
        "notes": """""",
    },
    {
        "title": 'Orange Cranberry Bundt Cake',
        "category": 'Cakes',
        "source": 'Inspired by Family Circle / Parents Magazine',
        "tags": ['vanilla', 'orange', 'cranberry'],
        "ingredients": """--- FOr the Cake ---
1 cup (2 sticks) unsalted butter, softened
2 cups sugar
4 eggs
1 tsp. vanilla extract
3 tsp. grated orange zest
2 ½ cups all-purpose flour
1 tsp. baking powder
1 tsp. salt
½ cup sour cream
1 ½ cups chopped cranberries (fresh or frozen or dry….can also use slightly less than 1.5)
--- FOr the Garnish and glaze ---
2-2 ½ cups of powdered sugar
4 tbsp. HOT water
1 egg white, lightly beaten (optional)
¼ cup sugar (optional)
Cranberries and strips of orange peel (optional)""",
        "instructions": """Preheat the oven to 350 degrees. Butter and flour Bundt pan.
Mix sugar and orange zest together and roll between fingers to release the oils.
Combine butter and sugar mixture in a large bowl. Cream, using paddle attachment, until light and fluffy. Add eggs, one at a time, mixing well and scraping the bowl after each addition. Add vanilla. Mix well.
Combine 2-1/2 cups of the flour, salt and baking powder in a bowl. Add half to butter mixture in bowl, then the sour cream, then remaining flour mixture, beating until smooth. Toss cranberries in some flour, and then fold into batter.
Pour into Bundt pan and bake at 350 degrees for 45 mins. Reduce temperature to 325 degrees and bake 20 minutes, or until a skewer inserted in the center comes out clean. Remove to a wire rack to cool completely (2-3 hours, should be cool to touch).
Place beaten egg white in a small bowl. Dip cranberries and orange peel in egg white, then in granulated sugar. Let dry on a plate.
Mix powdered sugar and hot water. It will be very thick. Use a spoon and pour on cake.""",
        "notes": """""",
    },
    {
        "title": 'Lemon Loaf',
        "category": 'Cakes',
        "source": 'Inspired by Plated Cravings Lemon Pound Cake',
        "tags": ['vanilla', 'lemon'],
        "ingredients": """--- FOr the Lemon Cake ---
1 ½ cups all-purpose flour
1 ½  tsp. baking powder
1 tbsp. lemon zest (about 1 lemon)
1 tsp. salt
½ cup unsalted butter, room temperature
¾ cup granulated sugar
2 large eggs, room temperature
1 tsp. vanilla extract
2 tbsp. lemon juice, about 1/2 lemon
½ cup buttermilk (120ml), room temperature
--- FOr the Lemon syrup ---
Juice of 1 lemon
3 tbsp. powdered sugar
--- FOr the Lemon Icing ---
Juice of 1 lemon
1 tbsp. milk or heavy cream
2+ cups powdered sugar""",
        "instructions": """Preheat the oven to 350 degrees. Butter 9 x 5 loaf pan.
In a small bowl combine flour and baking powder. In a large bowl, mix sugar and lemon zest together and roll between fingers to release the oils.
In the same large bowl, cream the butter and sugar together at medium-high speed until pale and fluffy, about 4-6 minutes. Scrape the sides of the bowl as needed. Add in eggs one at a time with mixer on low, then add vanilla and lemon juice. Mix all well together on medium-high.
With the mixer on low, add about one-third of the flour mixture and mix until almost combined, then add half the buttermilk and mix until just combined. Repeat with another third of flour mixture and then the last half of the buttermilk, ending with the last third of the flour. Beat until just incorporated.
Pour into loaf pan and bake at 350 degrees for 45-55 mins. Toothpick should come out clean.
Cool for 10 mins. Poke holes in the cake and drizzle the syrup onto the warm cake. Cool completely and then ice.
Squeeze the lemon, add milk, and 1 cup sugar. Keep adding more until it really thick. It should be able to droop off the whisk.""",
        "notes": """""",
    },
    {
        "title": 'Chocolate Chip Cookies',
        "category": 'Cookies',
        "source": '',
        "tags": ['chocolate', 'vanilla'],
        "ingredients": """--- INGREDIENTS – FOR THE Cookies ---
3 1⁄3 cups all purpose flour
1 ½ tsp. baking powder
1 ½ tsp. baking soda
1 tsp. salt
1 cup unsalted butter, melted and cooled
1 ½ cups packed brown sugar
½ cup white sugar
2 eggs
2 tsp. vanilla extract
12 oz. milk and semisweet chocolate chips
Pink Himalayan Salt""",
        "instructions": """Whisk together flour, baking powder, baking soda, and salt. Set aside.
In a stand mixer, beat together the melted butter, brown sugar, and white sugar on medium speed until lighter in color and fluffy, about 3 minutes.
Beat in eggs, one at a time.
Beat in vanilla extract.
Add all of the flour mixture at once and mix on low until just combined.
Mix in chocolate chips on low until just combined.
Scoop into balls with ice cream scooper and chill in fridge for at least one hour before baking or freeze them. (Chilled overnight is best – layer balls in a container separated by wax paper )
Bake them at 375 for 9 minutes, then rotate pan and bake for another 2-3 minutes.
Sprinkle with salt when they come out of the oven.
Let them sit on the pan to cool until they are easily removed by hand. One batch makes about 40-50 small to medium sized cookies.""",
        "notes": """""",
    },
    {
        "title": 'Levain Chocolate Chip Cookies',
        "category": 'Cookies',
        "source": 'Inspired by ModernHoney',
        "tags": ['chocolate', 'vanilla'],
        "ingredients": """--- INGREDIENTS – FOR THE Cookies ---
1 cup butter (cold and cut into small cubes)
1 cup brown sugar
½ cup sugar
2 eggs
1 tsp. vanilla
3 cups flour
1 tsp. cornstarch
¾ tsp. baking soda
¾ tsp. salt
2 cups chocolate chips
2 cups walnuts roughly chopped""",
        "instructions": """Preheat oven to 410 degrees.
In a large mixing bowl, cream together cold cubed butter, brown sugar, and sugar for 4 minutes or until creamy.
Add eggs, one at a time, mixing well after each one. Add vanilla.
Stir in flour, cornstarch, baking soda, and salt. Mix until just combined to avoid overmixing. Fold in chocolate chips and walnuts.
Separate dough into balls (about 30-32) and place on lightly colored cookie sheet. You can also make them really large like Levain, but then bake longer
Bake for 9-12 minutes or until golden brown on the top. Let them rest for at least 10 minutes to set.""",
        "notes": """""",
    },
    {
        "title": '“Skinny” Bagels',
        "category": 'Bread',
        "source": 'Inspired by SkinnyTaste Bagels. Weight Watchers friendly!',
        "tags": [],
        "ingredients": """--- INGREDIENTS – FOR THE Bagels ---
1 cup unbleached all purpose flour (whole wheat)
2 tsp. baking powder, make sure it's not expired or it won't rise
½ tsp. salt
1 cup non-fat Greek yogurt
optional toppings: everything bagel seasoning, sesame seeds, poppy seeds, dried garlic or onion flakes, jalapeños and cheese
Preheat oven to 375F. Place parchment paper or a silpat on a baking sheet. If using wax paper, spray with oil to avoid sticking.
In a medium bowl combine the flour, baking powder and salt and whisk well. Add the yogurt and mix with a fork or spatula until well combined, it will look like small crumbles.
Lightly dust flour on a work surface and remove dough from the bowl, knead the dough a few times until dough is tacky, but not sticky, about 15 turns (it should not leave dough on your hand when you pull away. I usually have to add some more flour).
Divide into 4 equal balls. Roll each ball into ¾ -inch thick ropes and join the ends to form bagels. (or you can make a ball and poke a hole in the center then stretch it slightly)
Top with water and sprinkle with seasoning of your choice.
OVEN METHOD: Bake at 375F on the top rack of the oven for 25 minutes. Let cool at least 15 minutes before cutting.
AIR FRYER METHOD: Preheat the air fryer 280F degrees. Transfer in batches without overcrowding and bake 15 to 16 minutes, or until golden. No need to turn. Let cool at least 15 minutes before cutting.""",
        "instructions": """""",
        "notes": """Makes 4 bagels. Recipe doubles well.
Freezes well. Put in microwave a bit to thaw and then can toast. Alternatively, you can also pre-slice and freeze. Then just toast right from freezer.
Must use Greek yogurt as regular yogurt has too much liquid and will make the dough sticky.""",
    },
    {
        "title": 'Oreo Truffles / Chai Truffles',
        "category": 'Candy & Truffles',
        "source": 'Inspired by several recipes…easiest dessert you will likely ever make!',
        "tags": ['chocolate', 'vanilla', 'chai', 'cream cheese', 'almond'],
        "ingredients": """--- INGREDIENTS – FOR THE Truffles ---
1-16oz package of Oreos – need 36 Oreos
1-8 oz cream cheese brick, softened
Chocolate or vanilla flavored almond bark (I prefer chocolate)
Optional toppings (gold sprinkles, nuts, crushed Oreos, etc)
Crush 36 cookies in a blender (works way better than rolling pin)
Add in cream cheese and make a mixture of the two. Should have a dough / paste-like consistency.
Make about 40-45 balls out of this mixture and put in fridge for at least 1 hour.
Melt almond bark in microwave in 30-second intervals, stirring in between.
Dip balls into melted bark and place on tray. Sprinkle any desired toppings on immediately.
Let truffles refrigerate for at least 1 hour.""",
        "instructions": """""",
        "notes": """An easy alternative to this is just take an Oreo and dip it in almond bark, add any desired toppings, and let it set in the fridge. Good for when you need to mail a treat!
Can replace these with pretty much any crushed cookies you like. I have made chai truffles (32 crushed Biscoff cookies, with about 1-1 ½ tsp. chai masala, mixed with 6 oz cream cheese, and coated in chocolate almond bark) as well!""",
    },
    {
        "title": 'Jalopeno-Almond Spaghetti',
        "category": 'Savory',
        "source": 'Inspired by the Chutney Life Jalapeño & Almond Pesto Spaghettini',
        "tags": ['almond'],
        "ingredients": """--- INGREDIENTS ---
½ box of spaghetti pasta, cooked until al dente
1 cup pecorino romano (parmesan works as well) cheese, shredded or grated
2 tbsp. extra virgin olive oil
2 tbsp. butter
1 cup reserved pasta water
4 cloves garlic, sliced thin
--- INGREDIENTS – FOR THE Pesto ---
3 jalapeños, cut in chunks (adjust according to spice level)
1 tsp salt
1/2 of a red onion (regular works fine too), cut in chunks
2 cloves garlic
1/4 cup sliced almonds
1/4 cup Extra virgin olive oil
Cook pasta according to package directions (leaving it slight undercooked). Reserve 1 cup of pasta water just before draining pasta and set aside.
To make the pesto, combine all the ingredients in a blender or food processor. Add in oil slowly if you can while keep the processor on.
In a large skillet, at the same time, add butter, olive oil and sliced garlic over medium heat. Do not let garlic brown, but let it soften. When garlic is fragrant, add the pesto to the skillet and stir for a few minutes. (I mix in some pasta waster into the pesto blender and add that in)
Add in the drained pasta, combine well. Add cheese and more pasta water in little bits until you get a nice creamy consistency.""",
        "instructions": """""",
        "notes": """Recipe doubles well and also works well for parties
Don’t use green onions. They will make the pesto taste bitter. Only red or sweet white onions.
If it gets dry or want to reheat large quantity, save some of the starchy water on the side for later use.""",
    },
    {
        "title": 'Eggplant Parmesan',
        "category": 'Savory',
        "source": 'Inspired by the Chutney Life Spicy Eggplant Parmesan',
        "tags": [],
        "ingredients": """--- INGREDIENTS ---
1 eggplant (about 1 lb.), sliced to ¼ inch slices
3 cups red sauce (I take any bottled sauce and heat it up with some fresh minced garlic, oregano, and Italian seasoning)
2 cups shredded Italian cheese blend (I use Mozzarella and Parmesan)
1-2 Jalepeños sliced (to put on top)
2-3 cups bread crumbs
--- INGREDIENTS – FOR THE Ricotta Mixture ---
Combine all the following ingredients in any blender until it’s a smooth mixture
1 ½ cups ricotta cheese
2 serrano peppers
½ cup green onions
2 tsp. garlic powder
1 tsp. oregano
½ tsp. salt
--- INGREDIENTS – FOR THE Chili Garlic Oil ---
My mom’s classic garlic oil. Heat all ingredients below on low in a small sauce pan for 5-10 minutes
1 cup extra virgin olive oil
½ stick unsalted butter
5-6 garlic cloves (minced)
2 tsp. crushed red pepper
2 tsp. garlic powder
2 tsp. oregano
1 tsp. salt and pepper""",
        "instructions": """Preheat oven to 375 Degrees.
Lay eggplant slices evenly spread apart on a baking sheet and sprinkle with salt and pepper on both sides. Then take a brush and liberally coat both sides with the chili garlic oil.
Bake eggplant for 30-40 minutes until cooked. Rotate pan once.
To assemble, layer the sauce, then eggplant, the ricotta mixture, and top with some cheese. Repeat layers. Top off with sliced jalapenos.
Bake covered for 15-20 minutes.
Take remaining chili garlic oil and use it to toast the bread crumbs for about 5 minutes.
Remove from oven and top with bread crumb mixture and broil for 3-5 minutes, uncovered.""",
        "notes": """""",
    },
    {
        "title": 'Eggless Cookies (Many flavors)',
        "category": 'Cookies',
        "source": 'Inspired by Hetal Vasavada Lemon & Cardamom Cookies',
        "tags": ['chocolate', 'vanilla', 'lemon', 'orange', 'cardamom', 'eggless'],
        "ingredients": """--- INGREDIENTS – FOR THE Cookies ---
1 cup + 2 tbsp. all-purpose flour
1 ½ tsp baking powder
¼ tsp salt
½ cup + 1 tbsp. granulated sugar
7 tbsp. unsalted butter, room temperature
½ tsp. vanilla extract
2 tbsp. milk
--- INGREDIENTS – FOR THE Flavorings ---
1⁄3 cup chocolate chips or
1 tsp. ground cardamom AND
1 ½ tbsp. granulated sugar or
1⁄3 cup white chocolate chips""",
        "instructions": """Zest of 3 mandarin orange AND
Zest of 1 Lemon AND
Zest of 3 key limes AND
Pre-heat oven to 375°F. Line a baking sheet with parchment paper.
In a small mixing bowl, whisk together flour, baking powder and salt. Set aside.
In a separate mixing bowl, add sugar and citrus zest. Use your fingers to rub the citrus zest and sugar together. Add butter and mix until well combined. Add vanilla and milk and mix again until well combined. Add dry ingredients and mix until you have a smooth dough. If using chips, gently mix them in now. Refrigerate the cookie dough for 10 minutes.
FOR LEMON & CARDAMOM COOKIES
In a small bowl, whisk together cardamom and sugar for coating.
Roll each cookie dough-ball into the cardamom sugar mixture until well coated. Bake for 13-15 minutes. Let the cookies cool on the cookie sheet for 3 minutes and then cool completely on a rack.
FOR ORANGE & CHOCOLATE OR LIME & WHITE CHOCOLATE COOKIES
Place each dough-ball onto cookie. Bake for 13-15 minutes. Sprinkle with salt as soon as they come out of the oven. Let the cookies cool on the cookie sheet for 3 minutes and then cool completely on a rack.""",
        "notes": """""",
    },
    {
        "title": 'My Mom’s Chutneys',
        "category": 'Savory',
        "source": '',
        "tags": ['lemon'],
        "ingredients": """--- INGREDIENTS-Garlic Chutney aka Lasanyu Marchu ---
Blend all ingredients below. DON’T add any water. It will take some time but worth it!
3-4 bulbs fresh garlic cloves
1 tsp. salt
3 tbsp. red chili powder
1 tsp. roasted cumin seeds
1 tbsp. sesame seeds
2 tbsp. olive oil
1 tsp. white vinegar
--- INGREDIENTS-Cilantro Chutney aka Dhana ni Chutney ---
Blend all ingredients below.
2-3 fresh garlic cloves
½ inch piece of fresh ginger
1-2 Green jalapenos
1 bunch cilantro (washed, shake out excess water)
1 tsp. Cumin seeds
Salt to taste
1 tsp. Lemon Juice
2 tbsp. Canola or Olive oil""",
        "instructions": """""",
        "notes": """""",
    },
    {
        "title": 'Spaghetti Squash Breadsticks',
        "category": 'Savory',
        "source": 'Inspired by Kirbie’s Cravings Breadsticks',
        "tags": ['almond'],
        "ingredients": """--- INGREDIENTS ---
1 Spaghetti squash (cooked and chopped)
1 large egg
1 cup shredded low fat mozzarella cheese divided
2 tsp. Italian seasoning
2 tsp. crushed red pepper
4 tbsp almond flour (can also use all-purpose flour)
3 tbsp shredded Parmesan cheese
Any garlic chutney / spread of your liking
Preheat oven to 450°F. Line a large baking sheet with parchment paper.
Chop cooked spaghetti squash so that pieces are no more than 1 inch long. Use a cheese cloth and  wring dry the spaghetti squash. When you are finished, you should have about 1 ½ cups of spaghetti squash.
Add spaghetti squash, egg, 1/4 cup mozzarella cheese, all seasonings, and almond flour to a large mixing bowl. Mix until all ingredients are thoroughly combined.
Dump squash mixture onto baking sheet lined with parchment paper. Using a spatula, spread out the batter so that it forms an oval that is approximately ¼ inch thick.
Bake in oven about 15 minutes or until edges are golden brown and the surface is dry to the touch.
Remove from oven and carefully flip over. Spread garlic spread on it. Sprinkle ¾ cup mozzarella cheese and 1/4 cup Parmesan cheese across the surface.
Lower oven temperature to 425°F. Bake for an additional 10-12 minutes or until cheese is melted and starts to blister and crust is crispy. Sprinkle parsley over breadsticks. Slice and serve with a dip of your choice. See some suggestions below!""",
        "instructions": """""",
        "notes": """""",
    },
    {
        "title": 'Red Velvet Cupcakes',
        "category": 'Cakes',
        "source": 'Inspired by Joy the Baker Red Velvet Cupcakes',
        "tags": ['vanilla', 'cream cheese'],
        "ingredients": """--- INGREDIENTS – FOR THE CAKE ---
4 Tbsp. unsalted butter, at room temperature
¾ cup sugar
1 egg
3 Tbsp. unsweetened cocoa powder
2 Tbsp. red food coloring
2 tsp. vanilla extract
½ cup buttermilk
1 cup plus 2 Tbsp. all-purpose flour
½ tsp. salt
½ tsp. baking soda
1 ½ teaspoons distilled white vinegar
--- For the Cream cheese Frosting ---
1-8 oz cream cheese bricks, chilled from fridge
½ cup (1 stick) unsalted butter, room temperature
1-1 ½ cups powdered sugar (used about 1 ¼ cups and worked well)
½ tablespoon vanilla extract
<    1⁄8 tsp. (small pinch) salt
Preheat the oven to 350 degrees.""",
        "instructions": """Cream the butter and sugar until light and fluffy, about three minutes.  Turn mixer to high and add the egg.  Scrape down the bowl and beat until well incorporated.
Red Velvet Paste: In a separate bowl mix together cocoa, vanilla and red food coloring to make a thick paste. Add to the batter and mix thoroughly.
Turn mixer to low and slowly add half of the buttermilk.  Add half of the flour and salt and mix until combined. Repeat with remaining ingredients. Beat on high until smooth.
Turn mixer to low and add baking soda and white vinegar.  Turn to high and beat a few more minutes. Batter should be light and fluffy!
Spoon into paper lined cupcake baking pan (about 2⁄3 of the way full) and bake at 350 F for 15-18 minutes or until a skewer inserted into the center cupcake comes out clean on top rack.
Let rest in the pan for 10 minutes, then place them of a cooling rack to cool completely and then frost.""",
        "notes": """Recipe can ½ well. For the egg, whisk it together and then use ½ and save rest for later!""",
    },
    {
        "title": 'Kati Rolls',
        "category": 'Savory',
        "source": 'Inspired by the chutney life Chicken Kati Rolls',
        "tags": [],
        "ingredients": """--- INGREDIENTS ---
1½ lbs skinless boneless chicken breasts or about 7 oz of paneer (both cut into small pieces)
1 small red onion, sliced
1 small bell pepper, sliced
2 tbsp. oil
1 tsp. cumin seeds
Kawan Brand Paranthas
1 tsp. Chaat Masala
--- INGREDIENTS – FOR the Marinade ---
1 tbsp. coriander-cumin powder
1 tsp. red chili powder
1 tsp. garam masala
1 tsp. fennel powder (whole fennel works fine too…rub between your fingers when adding into the bowl to release the aromas)
1 tsp. cumin powder
1 tbsp. Tandoori Masala (I recommend Swad or Rajah brand)
2-3 tbsp. yogurt
In a large bowl combine chicken / paneer with all ingredients listed under chicken marinade, mix well and set aside (If you can let marinate for at least 1 hour)
In a large skillet heat oil on medium heat and add cumin seeds. Once the cumin seeds begin to splutter, add the sliced onions and peppers and cook until slightly softened (about 3-5 minutes). Add chaat masala.
Add the chicken / paneer and cook, stirring occasionally until chicken is no longer pink (about 10-12 minutes) or the paneer is heated through fully.
Remove mixture from heat and set aside.
Heat up your choice of wrap (roti, frozen paratha etc), spread garlic chutney on cooked parantha, top with the mixture and fresh chopped cilantro, drizzle chutney and yogurt mixture, then wrap and serve!""",
        "instructions": """""",
        "notes": """I mix my mom’s cilantro chutney with some mayonnaise or hung Greek yogurt (if you don’t want to hang it then make sure it’s not too watery or it will make your parantha soggy) and spread it on top. The flavors are amazing!
Make sure to not add any salt to the marinade as the boxed chaat masala, tandoori masala, and garlic chutney all have salt in them already""",
    },
    {
        "title": 'Chocolate Cake',
        "category": 'Cakes',
        "source": 'Inspired by Love at first sight chocolate cake',
        "tags": ['chocolate', 'vanilla', 'coffee', 'almond', 'coconut'],
        "ingredients": """--- FOr the Cake ---
1 ¾ cup flour
1 ¾ cup sugar
¾ cup cocoa powder (unsweetened, I used Nestle)
2 tsp. baking soda
1 tsp. baking powder
1 tsp. salt
½ cup canola oil (coconut oil also works)
2 eggs
1 cup buttermilk
1 ½ tsp. vanilla
1 cup hot coffee (I take 1 cup water and about ½ tbsp. instant coffee powder)
Small piece of chocolate for shavings / garnish
Sliced / slivered almonds or walnuts (optional)
--- FOr the Buttercream ---
2 sticks of butter (softened)
~2 cups powdered sugar
~1 cup cocoa powder (unsweetened)
2-3 tbsp. milk / cream / half ‘n half (whatever you prefer. I typically use milk)
1-2 tsp. Vanilla""",
        "instructions": """Preheat oven to 350 degrees.
In a large bowl, stir together flour, sugar, cocoa, baking soda, baking powder, and salt. If you have a flour sifter, sift all dry ingredients.
In mixing bowl, beat (whisk is okay too) oil, eggs, buttermilk, and vanilla for 1 minute. Add dry ingredients to wet ingredients and stir until combined (be sure to not overmix). Pour in hot water and mix together. Add in nuts if want in cake. The batter will be liquidy but that's a good thing – it will create a moist cake.
Spray two 9-inch cake pans with non-stick cooking spray. You can also use three 8-inch cake pans for this recipe. Pour batter evenly into each pan. Bake at 22-27 (I baked for 23 mins) minutes. Place toothpick or cake tester in the center of the cake to check if it comes out clean.
Let cool before frosting.
In mixing bowl, cream all ingredients until light and fluffy. Use milk to obtain desired consistency. Frost cake only after it has cooled completely.
Placed a layer of nuts between each layer. Shave chocolate directly on top of cake to decorate.""",
        "notes": """""",
    },
    {
        "title": 'Funfetti Cake',
        "category": 'Cakes',
        "source": 'Inspired by Vanilla Cake and Milk Bar',
        "tags": ['vanilla', 'funfetti', 'cream cheese'],
        "ingredients": """--- INGREDIENTS – FOR THE CAKE ---
2 ½ cups all-purpose flour
2 ½ tsp. baking powder
½ tsp. salt
3/4 cups unsalted butter, softened to room temperature
1 ½ cups sugar
4 large eggs
1 tbsp. vanilla extract
1 1/4 cups milk
3 tbsp vegetable oil (or any flavorless oil, I used canola)
½ cup sprinkles
--- For the Cream cheese Frosting ---
2-8 oz cream cheese bricks, chilled from fridge
1 cup (2 sticks) unsalted butter, room temperature
2-3 cups powdered sugar (used about 2.5 cups and worked well)
1 tablespoon vanilla extract
1⁄8 tsp. (generous pinch) salt
--- FOr Milk bar style crumbs ---
½ cup sugar
1 ½ tbsp. brown sugar
¾ cup all-purpose flour
½ tsp. baking powder
¾ tsp. salt
2 tbsp. rainbow sprinkles
¼ cup vegetable oil / canola oil
1 tbsp. vanilla extract
--- FOr Milk Soak ---
½ cup milk
1 tsp. vanilla extract""",
        "instructions": """Preheat oven to 350°F/180 °C.
In a medium bowl, combine flour, baking powder, and salt. Set aside.
Add the butter, sugar, oil and vanilla extract to a large mixer bowl and beat together until light in color and fluffy, about 2-3 minutes. Do not skimp on the creaming time.
Add the eggs one at a time, mixing until mostly combined after each. Scrape down the sides of the bowl as needed to be sure all ingredients are well incorporated.
Add half of the dry ingredients to the batter and mix until mostly combined.
Slowly add the milk and mix until well combined. The batter will look curdled, but that’s ok.
Add the remaining dry ingredients and mix until well combined and smooth. Scrape down the sides of the bowl as needed to be sure all ingredients are well incorporated. Do not over mix the batter.
Divide the batter evenly between the cakes pans and bake for 22-25 minutes (I baked for 25), or until a toothpick comes out with a few crumbs. Let cool before frosting.
Preheat oven to 300°F and line a rimmed baking sheet with parchment paper.
Whisk together the sugars, flour, baking powder, salt, and sprinkles until combined.
Using an electric mixer on low, add the oil and vanilla and mix until it begins to come together and small clusters form.
Use your hands to make more clusters as needed, and transfer crumbs to the baking sheet. Bake for 20 minutes, stirring halfway through. Remove from the oven and allow to cool completely. If making the crumbs ahead of time, they can be stored for a few days in an airtight container at room temperature.
Mix the milk and vanilla together until well incorporated.
Cream together butter and cream cheese until well combined. Add in powdered sugar slowly (will look soft / smooth / velvety), vanilla, and salt until well combined.
Take the first layer of the cake and place it onto the desired plate / cake stand.
Poke some holes using a skewer or fork in the cake. Then using a brush liberally apply the milk soak mixture.
Then apply a thick layer of frosting and top with milk bar style crumbs.
Repeat this process from the remaining layers and garnish the top with more crumbs / frosting as you wish!
Recipe can be halved easily!""",
        "notes": """""",
    },
    {
        "title": 'Banana Bread',
        "category": 'Bread',
        "source": 'Inspired by Chrissy Teigen!',
        "tags": ['chocolate', 'vanilla', 'banana', 'coconut'],
        "ingredients": """--- INGREDIENTS ---
1 cup mashed very ripe bananas (about 3 bananas)
2 eggs
1⁄3 cup canola oil, plus a little more to grease the pan
1 cup all-purpose flour, plus a little more for dusting the pan
½ cup sugar
1 (1-oz) box vanilla instant pudding mix (sugar free is fine, but you can use regular if you like it a bit more sweet)
½ tsp. baking soda
¾ tsp. salt
½ cup sweetened shredded coconut (if using unsweetened then increase sugar to ¾ cup)
~½ cup dark chocolate chips
Salted butter, for serving
Preheat the oven to 325°F.
In a large bowl, mix the mashed bananas, eggs, and oil and set aside.
In another bowl, mix together the flour, baking soda, salt, sugar, and pudding mix. Mix the dry ingredients into the bowl of wet ingredients, but avoid using a mixer. Do this part manually to keep the end result nice and fluffy.
Add chocolate and shredded coconut to the batter, fold in gently.
Grease the loaf pan and pour batter in.
Bake until the cake bounces back when pressed or if a toothpick comes out clean when poked in. Depending on the pan, your baking time will vary, approximately 65-75 minutes. Let it cool for about 10 minutes and flip it onto a clean plate or tray for serving.
Enjoy it warm with butter or a scoop of ice cream! Keep it either refrigerated or left out in an airtight container.""",
        "instructions": """""",
        "notes": """This can be doubled and turned into a bundt cake as Chrissy Teigan does it! However, that portion was a bit too large for me so ½ works quite well.
The next day, warm the slice slightly in the microwave and eat with some salted spreadable butter on top.""",
    },
    {
        "title": 'Easy Cinnamon Rolls',
        "category": 'Bread',
        "source": 'Inspired by Jiffy®! Very simple but so delicious!',
        "tags": ['chai', 'cinnamon', 'easy'],
        "ingredients": """--- INGREDIENTS ---
2 cups “JIFFY” Baking Mix
2⁄3 cup milk
2 tbsp. margarine or butter, softened
3 tbsp. brown sugar
1 ½ tbsp. sugar
2 tsp. ground cinnamon
2 tsp. chai masala
Preheat the oven to 425°F.
Combine baking mix and milk. On floured surface, knead approximately 10 times or until dough is no longer sticky to the touch. Then roll out to a rectangle about ½ inch thick.
Spread butter onto the dough. Mix the cinnamon, sugars, chai masala together and sprinkle it evenly on top. It should be a fairly thick, but even layer.
Carefully, roll it up tightly. Cut the roll into even pieces.
Arrange the rolls onto a greased pan. Bake for 15-20 mins.
Frost with topping of your choice! Some ideas from me are below.""",
        "instructions": """""",
        "notes": """A cream cheese frosting would work well with this and resemble the “classic” glaze used on cinnamon rolls.
Melted Ghirardelli caramel chips, nuts (pecans or walnuts), powdered sugar glaze, melted Nutella are all good options for toppings as well.
For a less sweet glaze and flavor, add a bit more cardamom inside the cinnamon rolls and add orange zest into a powdered sugar glaze.""",
    },
    {
        "title": 'Gulab Jamun Bundt Cake',
        "category": 'Cakes',
        "source": 'Inspired by Milk and Cardamom',
        "tags": ['vanilla', 'lemon', 'cinnamon', 'cardamom', 'gulab jamun'],
        "ingredients": """--- FOr the Cake ---
2 sticks unsalted butter, softened, plus 1 tbsp., for greasing the Bundt pan
1 ⅓ cups all purpose flour
⅓ cup dried nonfat milk powder
1 cup granulated sugar
¾ tsp. ground cardamom
½ tsp. salt
1 tsp. vanilla extract
4 large eggs
1 cup pistachios for garnishing (optional)
--- FOr The Syrup ---
1 cup water
1 cup granulated sugar
½ teaspoon saffron thread
8 cardamom pods, slightly crushed (or ½ tsp. of ground cardamom)
1 cinnamon stick
½ to 1 tsp. rose water
2 tsp. fresh lime juice (or 1 tsp. lemon juice)
--- FOr The Glaze ---
~¼ cup syrup from above
1 cup powdered sugar
about 1-2 tsp. HOT water""",
        "instructions": """Preheat the oven to 325°F (163°C). Grease a 10-cup Bundt pan liberally with the 1 tbsp. of butter. In a medium bowl, whisk the flour and milk powder together until well combined.
Add the butter, sugar, and ground cardamom to a separate large bowl and mix with a hand mixer for 5-7 minutes; the butter will turn pale and fluffy. Add the salt and vanilla and stir to combine. Add 1 egg at a time, beating well between each addition. Add the flour mixture. Mix until the dry ingredients are just incorporated.
Spoon the batter into the Bundt pan and tap the pan on the counter 3–5 times to remove air bubbles. Bake the cake for 35–40 minutes (took 36 mins in my oven), or until a toothpick inserted into the center of the cake comes out clean.
10 minutes before the cake is done baking, make the syrup: Add the water, granulated sugar, saffron, cardamom pods, and cinnamon stick to a small saucepan. Bring to a boil over medium-high heat and simmer for 2 minutes. Remove the pot from the heat and whisk in the rose water and lime juice. Remove the cinnamon stick and cardamom pods from the syrup and discard. Reserve ¼ cup (60 ml) of the syrup and set aside.
Poke holes in the bottom of the Bundt cake with a fork. Pour the rest of the syrup over the Bundt cake while it is still warm in the pan. It will look like a lot of syrup, but the cake will soak it all up. Let the cake rest for 10 minutes, then invert it onto a serving platter.
In a medium bowl, whisk together the powdered sugar and reserved syrup to make a glaze. Add some hot water as need. It should be very thick.
Pour the glaze over the Bundt cake. Sprinkle with pistachios to garnish.""",
        "notes": """""",
    },
    {
        "title": 'Chai Cake',
        "category": 'Cakes',
        "source": 'Inspired by Liv for Cake',
        "tags": ['vanilla', 'chai', 'cinnamon', 'cardamom', 'cream cheese'],
        "ingredients": """--- INGREDIENTS – FOR THE CAKE ---
2 ¼ cups all-purpose flour
2 tsp. baking powder
3/4 tsp salt
1 ½ tsp ground cinnamon
1 tsp ground cardamom
½ tsp ground allspice
¼ tsp ground cloves
1 tsp ground ginger
¾ cup unsalted butter room temperature
1 cup granulated sugar
½ cups light brown sugar packed
3 large eggs room temperature
1 tsp vanilla
1.5 cup masala chai (use a thicker milk if possible)
--- For the Cream cheese Frosting ---
2-8 oz cream cheese bricks, chilled from fridge
1 cup (2 sticks) unsalted butter, room temperature
2-3 cups powdered sugar (used about 2.5 cups and worked well)
1 tablespoon vanilla extract
1⁄8 tsp. (generous pinch) salt
--- In a medium bowl, whisk flour, baking powder, spices, and salt until well combined. Set aside. ---
--- Reduce speed and add eggs one at a time fully incorporating after each addition. Add vanilla. ---
--- Alternate adding flour mixture and 1 cup Chai total. Mix very lightly to not over mix the flour. ---
--- Place cakes on wire rack to cool for 10mins then turn out onto wire rack. Allow to cool completely. Use remaining chai as a soak for the cake before frosting. ---""",
        "instructions": """Preheat oven to 350F. Grease and flour three 6" cake rounds or 24 cupcakes.
Cream butter and sugars on med-high until pale and fluffy.
Bake for 30-35 mins or until a toothpick inserted into the center comes out mostly clean. Bake cupcakes for about 16 mins.
Cream together butter and cream cheese until well combined. Add in powdered sugar slowly (will look soft / smooth / velvety), vanilla, and salt until well combined.""",
        "notes": """""",
    },
    {
        "title": 'Mango mousse Layered Cups',
        "category": 'Mousse & Cups',
        "source": 'Inspired by MyVegetarianRoots',
        "tags": ['lemon', 'mango', 'cardamom', 'cream cheese'],
        "ingredients": """--- For the Crust ---
4 packets parle g biscuits
½ cup (1 stick) unsalted butter, melted
¼ tsp ground cardamom
--- For the Whipped Cream ---
1¼ cup Full Fat Plain Whipping Cream
¼ cup Powdered Sugar
--- For the Cream cheese Mixture ---
3 cup Room Temp Full Fat Cream Cheese 3
¼ cup Room Temp Full Fat Sour Cream
¾ cup Sweetened Condensed Milk
1 tbsp Lemon Juice
¼ tsp Cardamom Powder
--- For the Layers ---
½ cup mango pulp
10 saffron strings
½ cup coarsely ground pistachios, ¼ for the mixture and ¼ for the layer in between""",
        "instructions": """Prepare the crust my mixing the cookies, cardamom, and butter in a food processor
Prepare cream cheese mixture by mixing all together, scrapping the sides of the bowl
Make whipped cream by beating until stiff peaks (4-6 mins approximately)
Mix the two, whipped cream and cream cheese mixture together (don’t overmix)
Split the mixture in ½, add mango and saffron to one and ground pistachios to the other. Don’t overmix.
Assemble the layers and let set for 10-12 hours and then garnish""",
        "notes": """The layers taste like Shrikand, so a great Diwali or Indian holiday dessert!""",
    },
    {
        "title": 'Orange Ombre Cake',
        "category": 'Cakes',
        "source": 'Inspired by Valerie Bertinelli',
        "tags": ['vanilla', 'orange'],
        "ingredients": """--- For the Orange Topping ---
4 tbsp unsalted butter, plus more for greasing pan
1 grapefruit
1 navel orange
1 Cara Cara orange
1 blood orange
½ cup sugar
¼ cup brown sugar
--- For the Cake ---
1¾ cups all purpose flour
1 tsp baking powder
½ tsp baking soda
½ tsp salt
1 stick unsalted butter, softened
1 cup granulated sugar
2 large eggs
1 tsp vanilla extract
1 cup buttermilk""",
        "instructions": """Preheat oven to 350F. Grease and flour 9in round pan
Zest 1 tsp from each fruit and reserve
Cut all the skin off and have then in mini squares (see above) and arrange them in the pan. About ¼ in thick
Mix the butter and sugars from the topping and then pour on top of the fruit
Take the sugar and mix the zest into it but rubbing it together to release the oils. Then add the butter and cream together about 3 minutes.
Add eggs one at a time. And then add the vanilla.
Whisk dry ingredients (flour, baking powder, baking soda, and salt together)
Add dry ingredients to egg mixture by alternating it with buttermilk. So flour, buttermilk, flour, buttermilk, flour. Mix until just combined.
Bake about 55 mins. Cool for 15 minutes, then invert it so the fruit is on top.""",
        "notes": """""",
    },
    {
        "title": 'Chai Tiramisu Cups',
        "category": 'Mousse & Cups',
        "source": 'Inspired by Little Sweet Baker',
        "tags": ['chocolate', 'vanilla', 'chai', 'cardamom'],
        "ingredients": """--- For the Base ---
Any soft sponge cake (I used bakery loaves from Wal-Mart
Strong chai to soak the cake in
--- For the Chai Cream ---
1 cup (250ml) whipping cream
1 cup (250g) mascarpone, softened
1/4 cup (50g) granulated sugar
1 tsp (5ml) vanilla extract
1 tsp cardamom (or more to taste)
1 tsp chai masala
Beat the whipping cream until medium-stiff peaks form. Set aside.
Mix the mascarpone, sugar, and vanilla until combined. Add in the whipped cream. Use a rubber spatula and fold the mixture a few times scraping the bottom and sides of the bowl. Then use the electric mixer to beat again until smooth. Add spices.
Dip the cake in the chai first, then add the flavored cream, then add sprinkle cocoa+chai powder on top, then finally garnish with chocolate chai truffle (optional)""",
        "instructions": """""",
        "notes": """Truffle on top is really nice touch and elevates the dessert, could also top with Parle G
Also make with cookie dough (spiced with chai masala) and then add melted chocolate one top that has spices in it and put in fridge to set. Turns out really good for a bigger dessert.""",
    },
    {
        "title": 'Blueberry Muffins',
        "category": 'Muffins',
        "source": 'Inspired by Sally’s Baking Addiction',
        "tags": ['vanilla', 'blueberry', 'cinnamon', 'banana'],
        "ingredients": """--- For the Topping ---
½ cup brown sugar
½ chopped walnuts
1 tsp cinnamon
--- For The muffins ---
1 cup whipping cream
1 and 3/4 cups all-purpose flour
1 tsp baking soda
1 tsp baking powder
1/2 tsp salt
1/2 cup (8 Tbsp) unsalted butter, softened to room temperature
1/4 cup granulated sugar
1/4 cup packed light or dark brown sugar
2 large eggs
2 tsp vanilla
3/4 cup buttermilk (~2.25 tsp vinegar + milk to make 3/4 cup)
1 mashed banana
1 and 1/2 cups fresh or frozen blueberries
Preheat oven to 425 F and grease muffin pan with pam.
Mix all the topping ingredients together and set aside. Mix all the dry ingredients together and set aside.
Using handheld or paddle / whisk attachment, beat the butter, and sugars together on high speed until smooth and creamy (2+ mins). On medium speed at egg one at a time and mix well after each egg. Add in vanilla and mashed banana. Beat well.
Remove from mixer and in dry ingredients and buttermilk and mix until just combined. Fold in the berries.
Spoon batter into cups (1-2 spoon almost to the top). Spoon the topping on top and gently press down to the surface to it sticks with back of spoon.
Bake for 5 mins at 425. Then keep oven closed, reduce to 350 for 18 mins. ½ way through rotate the pan. Check with toothpick to ensure comes out clean""",
        "instructions": """""",
        "notes": """""",
    },
    {
        "title": 'Brownies',
        "category": 'Brownies',
        "source": 'Inspired by King Arthur',
        "tags": ['chocolate', 'vanilla', 'espresso'],
        "ingredients": """4 large eggs
1 1/4 cups cocoa
1 tsp table salt
1 tsp baking powder
1 tsp baking soda
1 tsp espresso powder, optional for enhanced flavor
1 tbsp King Arthur Pure Vanilla Extract
16 tbsp unsalted butter
2 cups granulated sugar
1 1/2 cups King Arthur Unbleached All-Purpose Flour
2 cups chocolate chips""",
        "instructions": """Preheat the oven to 350°F. Lightly grease a 9" x 13" pan.
Crack the 4 eggs into a bowl, and beat them at medium speed with the cocoa, salt, baking powder, espresso powder, and vanilla for about 1 minute, or until smooth. You can do this while you're melting your butter (next step).
In a medium-sized microwave-safe bowl, or in a saucepan set over low heat, melt the butter, then add the sugar and stir to combine. Or simply combine the butter and sugar, and heat, stirring, until the butter is melted. Continue to heat (or microwave) briefly, just until the mixture is hot (about 110°F to 120°F), but not bubbling; it'll become shiny looking as you stir it. Heating the mixture to this point will dissolve more of the sugar, which will help produce a shiny top crust on your brownies.
Add the hot butter/sugar mixture to the egg/cocoa mixture, stirring until smooth.
Add the flour and chips, stirring until smooth. Again, adding the chips helps produce a shiny top crust.
Bake the brownies for 28 to 32 minutes, until the edges feel set, and the center should look very moist, but not uncooked. When testing to see if brownies are done, take a toothpick or the tip of a sharp knife and carefully poke it into the center of the pan, digging around just enough to see the interior. You should see moist crumbs, but no uncooked batter. Yes, you'll be left with a small divot in the center of your brownies; just cut around it when you're cutting the brownies into squares.""",
        "notes": """""",
    },
    {
        "title": 'Lemon Cheesecake',
        "category": 'Cheesecake',
        "source": 'Inspired by Zoha and Natasha’s Kitchen',
        "tags": ['vanilla', 'lemon', 'cream cheese', 'cheesecake'],
        "ingredients": """--- For the Crust ---
19.5 full sheets of graham crackers
pinch of salt
1.5 (1 tbsp less is also ok and then slowly add until crust holds shape) sticks of melted butter
--- For the Filling ---
800g cream cheese (28 oz or 3.5 8 oz packs), room temperature
150g granulated sugar (⅔ cup)
1 tbsp lemon zest
2 teaspoon vanilla bean paste (1-2 pods and then 1 tsp vanilla extract)
½ teaspoon salt
3 tbsp lemon juice
120g sour cream (½ cup)
120g heavy cream (½ cup), chilled
--- For the Curd Topping ---
3 large eggs
½ cup granulated sugar
pinch of fine sea salt
1 tsp grated lemon zest, from 1 medium lemon
1/2 cup fresh lemon juice, from 3 lemons, strained
6 Tbsp unsalted butter, cut into small pieces
½ tsp vanilla extract
--- Crust (this is a thick crust) ---
--- Filling ---""",
        "instructions": """For the crust, grind the graham crackers, then add the melted butter and salt and mix
Line a 9” springform pan with parchment paper, tightly pack the crust, level and place in fridge
Use the paddle attachment of a stand mixer to mix the sugar and zest together to release oils. Cream cheese, sugar, vanilla and salt until creamy and the sugar is dissolved (<2 minutes)
Add in the sour cream and lemon juice, and mix until combined
Separately, whisk the heavy cream until it reaches stiff peaks and gently fold into cream cheese mixture
Pour the cheesecake filling and press it down with an offset spatula to remove any air bubbles and spread evenly. Place in fridge for 4 hours (or overnight) until fully set
Electric whisk eggs, sugar, zest, salt until light and frothy. Add lemon juice.
Add butter and begin to heat on medium for ~10 mins. Temp should be around 165-170. Once bubbles around edges take off heat, it will thicken once cool.
Pass through sieve, add vanilla, and store
Decorate with whipped topping
½ cup heavy cream (chilled), 1 tbsp powdered sugar, ½ tsp vanilla – beat until stiff peaks""",
        "notes": """""",
    },
    {
        "title": 'Lemon Blueberry Basil Loaf Cake',
        "category": 'Cakes',
        "source": '',
        "tags": ['vanilla', 'lemon', 'blueberry'],
        "ingredients": """--- FOr the Cake ---
½ cup (1 stick) unsalted butter, softened
1 cup sugar
2 eggs
½ tsp. vanilla extract
1.5 tsp. grated lemon zest (1.5 lemons)
1 ¼cups all-purpose flour
½ tsp. baking powder
½ tsp. salt
¼ cup sour cream
¼ cup chopped basil
--- FOr the glaze ---
1 cup of powdered sugar
2-3 tbsp. HOT water with basil leaves soaked in it
pinch of lemon juice
--- FOr the Jam (heat all up in sauce pan 8-10 mins) ---
1 cup fresh blueberries
1 tbsp. sugar
Zest of ½ lemon
Juice of ½ lemon
2 tbsp + 1 tbsp chopped basil (mix in some fresh at the end)
½ tsp corn starch""",
        "instructions": """Preheat the oven to 350 degrees. Butter and flour loaf pan.
Mix sugar and lemon zest together and roll between fingers to release the oils.
Combine butter and sugar mixture in a large bowl. Cream, using paddle attachment, until light and fluffy. Add eggs, one at a time, mixing well each time. Add vanilla. Mix well again.
Combine 2-1/2 cups of the flour, chopped basil, salt and baking powder in a bowl. Add half to butter mixture in bowl, then the sour cream, then remaining flour mixture, beating until smooth.
Pour into ½ mixture into loaf pan, then spread the cooled jam, then the remaining batter and bake at 350 degrees for 30 mins. Reduce temperature to 325 degrees and bake 15 minutes, or until a skewer inserted in the center comes out clean. Remove to a wire rack to cool completely (2-3 hours, should be cool to touch).""",
        "notes": """""",
    },
    {
        "title": 'Chocolate Babka',
        "category": 'Bread',
        "source": 'Inspired by Preppy Kitchen',
        "tags": ['chocolate'],
        "ingredients": """--- FOr the Dough ---
270g all-purpose flour (2 ¼ cups)
50g granulated sugar (½ cup)
½ pkt teaspoons instant yeast (1/2 .25-ounce packet)
4 large eggs room temperature
2 oz whole milk (100 degrees)
¾ teaspoons kosher salt
5 tablespoons unsalted butter room temperature
--- FOr the Filling ---
4 tbsp butter
4 oz chocolate / chocolate chips
--- FOr the Glaze ---
Equal parts sugar and water (simmer but it will thicken so do it and immediately spread on hot babka)""",
        "instructions": """Whisk together the flour, sugar, and yeast in the bowl of a stand mixer. Add the eggs, milk, and salt and mix on low speed using the dough hook attachment until combined and a dough starts to form, for about 2 minutes.
Add the butter a tablespoon or so at a time, waiting for the butter to be incorporated before adding more. Once all the butter has been added, continue kneading until a smooth elastic dough forms, about 10 minutes, scraping down the sides of the bowl occasionally. The dough will still feel sticky but will be very stretchy.
Transfer the dough to a large oiled bowl, turning to coat. Then cover and chill overnight or for at least 8 hours.
Roll out the dough on oiled surface pretty thin and then spread the chocolate filling end to end. I also sprinkled chocolate chips. Roll it up on the horizontal side tightly. Cut in ½ and braid.
Proof for another 1.5-2 hours (I did in oven with boiling water).
Bake at 350 degrees for 40 mins (inside temp should be 88 C) in buttered and flours loaf pan.
Glaze immediately after with syrup and slice once cooled a bit in pan""",
        "notes": """""",
    },
    {
        "title": 'Spiced Blackberry and Pear Cobbler',
        "category": 'Cobblers & Crisps',
        "source": 'Inspired by Sally Baking',
        "tags": ['vanilla', 'lemon', 'pear', 'blackberry', 'cinnamon', 'cardamom'],
        "ingredients": """--- FOr the Topping ---
1 cup (125g) all-purpose flour
½ cup (100g) brown sugar (packed)
1 tsp baking powder
1 tsp cinnamon
1/8 tsp salt
6 tbsp (85g) unsalted butter, melted and slightly cooled
--- FOr the Filling ---
5 cups (700g) chopped, peeled fresh pears (Bosc or Bartlett and should be firm)
2 cups (300g) fresh blackberries (halved if large)
6 tbsp (75g) granulated sugar
¼ cup (31g) all-purpose flour
½ tsp ginger
½ tsp cinnamon
¼ tsp nutmeg
¼ tsp cardamom
1 tsp lemon juice
1 tsp vanilla
Preheat over at 375 and grease pan. I did small ramekins and ½ recipe.
For the topping, mix it all together with a fork and put in fridge. Don’t crumble it too much as the big bits taste good on the top crumble
For the filling, mix all the dry ingredients together. Then peel and cut the pears in ½ inch chunks and halve blackberries if needed. Add the lemon and vanilla. Can set all in fridge at this step if needed. Then just mix it all together when ready to bake. Its about 125g fruit to 14-15g dry mixture (for ramekins).
Fill the container with fruit mixture and top with chilled topping. Bake for 40-50 mins or until juice is bubbly and top is brown. I also covered with lid about after 25-30 mins so that it doesn’t over brown on the top.
Store in fridge covered for 4 ish days.""",
        "instructions": """""",
        "notes": """""",
    },
]


def seed_database() -> int:
    """Seed the database with recipes. Returns count of inserted recipes."""
    init_db()
    existing = {r["title"].lower() for r in get_all_recipes()}
    count = 0
    for recipe in RECIPES:
        if recipe["title"].lower() not in existing:
            add_recipe(**{k: v for k, v in recipe.items() if k != "date_added"})
            count += 1
    return count


if __name__ == "__main__":
    n = seed_database()
    print(f"Seeded {n} recipes.")
